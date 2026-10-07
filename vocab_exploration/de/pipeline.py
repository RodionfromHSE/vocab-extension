#!/usr/bin/env python3
"""German vocabulary pipeline: word list → enriched JSON → audio → Anki package (.apkg).

Stages (all resumable; re-running only does missing work):
  words   .txt → words.json
  meta    words.json → enriched.json   (parallel Fireworks calls, cached per word in meta_cache.jsonl)
  cards   enriched.json → cards.json    (one record per note, one key per Anki field)
  audio   cards.json → cards_with_audio.json  (gTTS de: word, example 1, example 2 → media/)
  export  → deck.apkg (note type + notes + audio), cards_final.json, preview.md
  anki    import deck.apkg via AnkiConnect (only with --to-anki)
"""

import argparse
import json
import os
import random
import subprocess
import sys
import threading
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from omegaconf import OmegaConf
from tqdm import tqdm

DE_DIR = Path(__file__).resolve().parent
ROOT = DE_DIR.parent.parent
sys.path.insert(0, str(ROOT / "meta_generator"))
sys.path.insert(0, str(ROOT))

from main import create_components
from run_pipeline import ensure_anki_running
from src.utils.config import read_config

from cards import to_note_record, with_sound_fields, write_apkg
from render_markdown import render
from txt_to_json import load_words, spelling_hint

COST_PER_WORD_USD = 0.002  # deepseek-v4p1-flash, measured in eval/
AUDIO_PASSES = (("word_", "tts_text"), ("example1_", "example1_de"), ("example2_", "example2_de"))
ANKI_CONNECT_URL = "http://127.0.0.1:8765"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ---------- words ----------

def stage_words(config: Any, run_dir: Path, sample: int | None, seed: int) -> list[dict[str, str]]:
    words = load_words(Path(config.input_txt))
    if sample:
        words = random.Random(seed).sample(words, sample)
    entries = [{"word": word, "context": spelling_hint(word)} for word in words]
    write_json(run_dir / "words.json", entries)
    print(f"[words] {len(entries)} words")
    return entries


# ---------- meta ----------

def load_meta_cache(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    rows = (json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line)
    return {row["word"]: row["entry"] for row in rows}


def generate_missing(handler: Any, todo: list[dict[str, str]], cache_path: Path, workers: int) -> dict[str, str]:
    """Generate entries in parallel, appending each success to the cache; returns failures."""
    lock = threading.Lock()
    failures: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=workers) as pool, cache_path.open("a", encoding="utf-8") as cache:
        futures = {pool.submit(handler.handle, item): item["word"] for item in todo}
        for future in tqdm(as_completed(futures), total=len(futures), desc="[meta]"):
            word = futures[future]
            try:
                line = json.dumps({"word": word, "entry": future.result()}, ensure_ascii=False)
            except Exception as exc:
                failures[word] = f"{type(exc).__name__}: {exc}"
                continue
            with lock:
                cache.write(line + "\n")
                cache.flush()
    return failures


def stage_meta(config: Any, run_dir: Path, words: list[dict[str, str]]) -> list[dict[str, Any]]:
    cache_path = run_dir / "meta_cache.jsonl"
    todo = [item for item in words if item["word"] not in load_meta_cache(cache_path)]
    print(f"[meta] {len(words) - len(todo)} cached, {len(todo)} to generate (~${len(todo) * COST_PER_WORD_USD:.2f})")
    if todo:
        _, _, _, _, handler = create_components(read_config(config.meta.config_file))
        failures = generate_missing(handler, todo, cache_path, config.meta.workers)
        write_json(run_dir / "failed.json", failures)
        if failures:
            print(f"[meta] {len(failures)} failed (see failed.json; re-run to retry)")

    cache = load_meta_cache(cache_path)
    enriched = [cache[item["word"]] for item in words if item["word"] in cache]
    write_json(run_dir / "enriched.json", enriched)
    return enriched


# ---------- cards ----------

def stage_cards(config: Any, run_dir: Path, enriched: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = [to_note_record(entry, list(config.cards.tags)) for entry in enriched]
    write_json(run_dir / "cards.json", records)
    print(f"[cards] {len(records)} notes")
    return records


# ---------- audio ----------

def run_audio_pass(config: Any, run_dir: Path, records: list[dict[str, Any]], key_prefix: str, text_key: str) -> list[dict[str, Any]]:
    """Run audio_component once (one text field → one set of `<prefix>audio_*` keys)."""
    name = key_prefix.rstrip("_")
    input_path, output_path = run_dir / f"audio_{name}_in.json", run_dir / f"audio_{name}_out.json"
    audio_config = run_dir / f"audio_{name}.yaml"
    OmegaConf.save(
        {
            "language": config.audio.language,
            "text_key": text_key,
            "output_key_prefix": key_prefix,
            "save_directory": config.audio.media_dir,
            "media_subdirectory": "",
            "filename_prefix": f"{config.audio.filename_prefix}{key_prefix}",
        },
        audio_config,
    )
    write_json(input_path, records)
    subprocess.run(
        [sys.executable, "main.py", str(input_path), "-o", str(output_path), "-c", str(audio_config)],
        cwd=ROOT / "audio_component",
        check=True,
    )
    return read_json(output_path)


def audio_keys(record: dict[str, Any]) -> dict[str, str]:
    return {key: value for key, value in record.items() if "_audio_" in key and key.endswith("_path")}


def has_required_audio(record: dict[str, Any]) -> bool:
    return all(f"{prefix}audio_relative_path" in record for prefix in ("word_", "example1_"))


def stage_audio(config: Any, run_dir: Path, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Generate audio only for words without it yet, then merge with previous runs."""
    output_path = run_dir / "cards_with_audio.json"
    previous = read_json(output_path) if output_path.exists() else []
    done = {r["word"]: audio_keys(r) for r in previous if has_required_audio(r)}  # failed audio → redo
    todo = {record["word"]: dict(record) for record in records if record["word"] not in done}
    print(f"[audio] {len(done)} already voiced, {len(todo)} to generate")

    for key_prefix, text_key in AUDIO_PASSES:
        subset = [record for record in todo.values() if record.get(text_key)]  # e.g. no 2nd example
        if subset:
            for voiced in run_audio_pass(config, run_dir, subset, key_prefix, text_key):
                todo[voiced["word"]].update(audio_keys(voiced))

    audio_by_word = done | {word: audio_keys(record) for word, record in todo.items()}
    merged = [{**record, **audio_by_word.get(record["word"], {})} for record in records]
    write_json(output_path, merged)
    return merged


# ---------- export / anki ----------

def stage_export(config: Any, run_dir: Path, records: list[dict[str, Any]]) -> Path:
    final = [with_sound_fields(record) for record in records]
    write_json(run_dir / "cards_final.json", final)

    apkg_path = run_dir / "deck.apkg"
    media_dir = Path(config.audio.media_dir).expanduser()
    notes = write_apkg(final, config.cards.deck_name, media_dir, apkg_path)
    preview = render([record["entry"] for record in final], f"{config.run_name} · {len(final)} words")
    (run_dir / "preview.md").write_text(preview, encoding="utf-8")

    missing_audio = sum(not record["word_audio"] or not record["example1_audio"] for record in final)
    print(f"[export] {notes} notes → deck.apkg, preview.md ({missing_audio} notes missing audio)")
    return apkg_path


def anki_connect(action: str, **params: Any) -> Any:
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    request = urllib.request.Request(ANKI_CONNECT_URL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=600) as response:
        reply = json.loads(response.read())
    if reply.get("error"):
        raise RuntimeError(f"AnkiConnect {action}: {reply['error']}")
    return reply["result"]


def stage_anki(apkg_path: Path) -> None:
    ensure_anki_running()
    anki_connect("importPackage", path=str(apkg_path))
    print(f"[anki] imported {apkg_path.name} via AnkiConnect")


# ---------- main ----------

def preflight(config: Any) -> None:
    """Fail fast (before any paid call) on missing key or input."""
    problems = []
    if not os.environ.get("FIREWORKS_API_KEY"):
        problems.append("FIREWORKS_API_KEY is not set (run `source ~/.zshrc` or export it)")
    if not Path(config.input_txt).exists():
        problems.append(f"input_txt not found: {config.input_txt}")
    if problems:
        sys.exit("Preflight failed:\n  - " + "\n  - ".join(problems))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", type=Path, default=DE_DIR / "pipeline_config.yaml")
    parser.add_argument("--run-name", help="Override run_name (separate run dir + caches)")
    parser.add_argument("--sample", type=int, help="Random subsample of the word list (for tests)")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--skip-audio", action="store_true", help="No TTS (cards get no [sound:])")
    parser.add_argument("--to-anki", action="store_true", help="Also import deck.apkg via AnkiConnect")
    return parser.parse_args()


def load_pipeline_config(args: argparse.Namespace) -> Any:
    config = OmegaConf.load(args.config)
    if args.run_name:
        config.run_name = args.run_name
    OmegaConf.resolve(config)
    return config


def main() -> None:
    args = parse_args()
    config = load_pipeline_config(args)
    preflight(config)
    run_dir = Path(config.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"Run dir: {run_dir}")

    words = stage_words(config, run_dir, args.sample, args.seed)
    enriched = stage_meta(config, run_dir, words)
    records = stage_cards(config, run_dir, enriched)
    if not args.skip_audio:
        records = stage_audio(config, run_dir, records)
    apkg_path = stage_export(config, run_dir, records)
    if args.to_anki:
        stage_anki(apkg_path)


if __name__ == "__main__":
    main()

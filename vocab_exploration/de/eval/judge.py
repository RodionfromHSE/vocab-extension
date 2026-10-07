#!/usr/bin/env python3
"""Blind LLM-as-judge over bake-off outputs.

For every word, all candidate outputs are anonymized (A/B/C, shuffled per word)
and judged against the Cambridge entry by every judge model. The scorer later
drops self-judgments, so each output is rated only by the *other* models.
"""

import argparse
import hashlib
import json
import logging
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from omegaconf import OmegaConf

EVAL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EVAL_DIR))

from run_bakeoff import MODELS, META_ROOT, MeteredModel, ModelSpec

sys.path.insert(0, str(META_ROOT))
from src.model.fireworks_model import FireworksModel
from src.processors.codeblock_extractor_processor import CodeBlockExtractorProcessor
from src.utils.smart_format import smart_format

GOLD_KEYS = (
    "headword", "pos", "article", "genitive", "plural", "praesens_3sg", "praeteritum",
    "partizip_2", "perfekt_mit_sein", "sense_info", "definition_de", "translations_en", "examples",
)
SCORE_KEYS = (
    "sense_matches_cambridge", "sense_is_most_common", "word_en_ok", "definitions_ok",
    "examples_naturalness", "translations_ok", "grammar_errors", "comment",
)
MAX_ATTEMPTS = 3
JUDGE_CACHE_DIR = EVAL_DIR / "judge_cache"


def load_results(results_dir: Path, model_names: list[str]) -> dict[str, list[dict[str, Any]]]:
    return {
        name: json.loads((results_dir / f"{name}.json").read_text(encoding="utf-8"))["results"]
        for name in model_names
    }


def anonymize(word_index: int, outputs: dict[str, Any], seed: int) -> dict[str, str]:
    """Return {candidate_id: model_name}, shuffled deterministically per word."""
    names = sorted(name for name, output in outputs.items() if output is not None)
    random.Random(seed * 1000 + word_index).shuffle(names)
    return {chr(ord("A") + index): name for index, name in enumerate(names)}


def build_prompt(template: str, gold: dict[str, Any], candidates: dict[str, Any]) -> str:
    gold_view = {key: gold.get(key) for key in GOLD_KEYS}
    return smart_format(
        template,
        {
            "gold": json.dumps(gold_view, indent=2, ensure_ascii=False),
            "candidates": json.dumps(candidates, indent=2, ensure_ascii=False),
        },
    )


def is_complete(judgment: Any, candidate_ids: list[str]) -> bool:
    return isinstance(judgment, dict) and all(
        isinstance(judgment.get(cid), dict) and all(key in judgment[cid] for key in SCORE_KEYS)
        for cid in candidate_ids
    )


def judge_once(
    model: MeteredModel, processor: CodeBlockExtractorProcessor, prompt: str, ids: list[str]
) -> dict[str, Any] | None:
    """Ask the judge until it returns scores for every candidate; None on failure."""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            raw = model.generate(prompt)
            judgment = processor.process(raw)
            if is_complete(judgment, ids):
                return judgment
            print(f"  attempt {attempt}: incomplete judgment: {raw[-300:]!r}", file=sys.stderr)
        except Exception as exc:
            print(f"  attempt {attempt}: {type(exc).__name__}: {exc}", file=sys.stderr)
        time.sleep(2)
    return None


def cached_judgment(cache_file: Path, compute) -> dict[str, Any] | None:
    """Reuse a stored judgment so interrupted runs resume where they stopped."""
    if cache_file.exists():
        return json.loads(cache_file.read_text(encoding="utf-8"))
    judgment = compute()
    if judgment is not None:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(judgment, indent=2, ensure_ascii=False), encoding="utf-8")
    return judgment


def build_judge(spec: ModelSpec, effort: str) -> MeteredModel:
    config = OmegaConf.create(
        {
            "api": {
                "type": "fireworks",
                "model": spec.model_id,
                "params": {"temperature": 0.0, "max_tokens": 16384, "timeout": 300, "reasoning_effort": effort},
            }
        }
    )
    return MeteredModel(FireworksModel(config))


def run_judge(
    spec: ModelSpec,
    effort: str,
    template: str,
    gold: list[dict[str, Any]],
    results: dict[str, list[dict[str, Any]]],
    seed: int,
) -> dict[str, Any]:
    """Judge every word with one judge model; returns per-word scores by model name."""
    model = build_judge(spec, effort)
    processor = CodeBlockExtractorProcessor({}, extract_json=True)
    per_word = []
    for index, gold_entry in enumerate(gold):
        outputs = {name: rows[index]["output"] for name, rows in results.items()}
        mapping = anonymize(index, outputs, seed)
        candidates = {cid: outputs[name] for cid, name in mapping.items()}
        prompt = build_prompt(template, gold_entry, candidates)
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()[:12]  # new outputs → new cache entry
        cache_file = JUDGE_CACHE_DIR / spec.name / f"{index:03d}_{gold_entry['query']}_{prompt_hash}.json"
        judgment = cached_judgment(cache_file, lambda: judge_once(model, processor, prompt, list(mapping)))
        per_word.append({mapping[cid]: judgment[cid] for cid in mapping} if judgment else {})
        status = "ok" if judgment else "FAILED"
        print(f"[judge {spec.name}] {index + 1}/{len(gold)} {gold_entry['query']}: {status}", flush=True)
    cost = model.totals.cost(spec.pricing)
    return {"scores": per_word, "calls": model.totals.calls, "cost_usd": round(cost, 6)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold", type=Path, default=EVAL_DIR / "gold.json")
    parser.add_argument("--results-dir", type=Path, default=EVAL_DIR / "results")
    parser.add_argument("--output", type=Path, default=EVAL_DIR / "judgments.json")
    parser.add_argument("--judges", nargs="+", choices=sorted(MODELS), default=list(MODELS))
    parser.add_argument("--reasoning-effort", choices=("low", "medium", "high"), default="medium")
    parser.add_argument("--seed", type=int, default=7)
    return parser.parse_args()


def main() -> None:
    logging.getLogger().setLevel(logging.CRITICAL)
    args = parse_args()
    gold = json.loads(args.gold.read_text(encoding="utf-8"))
    results = load_results(args.results_dir, list(MODELS))
    template = (EVAL_DIR / "judge_prompt.md").read_text(encoding="utf-8")

    with ThreadPoolExecutor(max_workers=len(args.judges)) as pool:
        futures = {
            name: pool.submit(run_judge, MODELS[name], args.reasoning_effort, template, gold, results, args.seed)
            for name in args.judges
        }
        judgments = {name: future.result() for name, future in futures.items()}

    payload = {"words": [entry["query"] for entry in gold], "judges": judgments}
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build a stratified eval set (words + Cambridge gold) from the German word list.

Words are drawn in random (seeded) order and looked up on Cambridge until every
POS bucket is full. Only entries from the GLOBAL dictionary with an exact or
phrase match are kept, so every gold item has grammar + German definition.
"""

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any

EVAL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EVAL_DIR.parent))

from scrape_cambridge import scrape
from txt_to_json import load_words, spelling_hint, FEW_SHOT_WORDS

DEFAULT_QUOTAS = {"noun": 10, "verb": 8, "adjective_adverb": 4, "phrase": 3}


def bucket_for(word: str, gold: dict[str, Any]) -> str | None:
    """Map a Cambridge entry to a stratification bucket (None = unusable)."""
    if gold.get("source") != "global" or gold.get("match") not in {"exact", "phrase"}:
        return None
    if " " in word:
        return "phrase"
    if gold["pos"] in {"adjective", "adverb"}:
        return "adjective_adverb"
    if gold["pos"] in {"noun", "verb"}:
        return gold["pos"]
    return None


def possible_buckets(word: str) -> set[str]:
    """Cheap pre-scrape guess of which buckets a word could land in."""
    if " " in word:
        return {"phrase"}
    if word[0].isupper():
        return {"noun"}
    return {"verb", "adjective_adverb"}


def collect(words: list[str], quotas: dict[str, int]) -> list[dict[str, Any]]:
    """Scrape words until all quotas are met; return gold entries with buckets."""
    remaining = dict(quotas)
    selected = []
    for word in words:
        if not any(remaining.values()):
            break
        if not any(remaining[bucket] for bucket in possible_buckets(word)):
            continue  # skip a Cambridge request we almost certainly can't use
        gold = scrape(word)
        bucket = bucket_for(word, gold)
        if bucket is None or not remaining[bucket]:
            continue
        remaining[bucket] -= 1
        selected.append({**gold, "bucket": bucket})
        print(f"[{bucket}] {word}")

    if any(remaining.values()):
        print(f"Warning: unfilled quotas {remaining}", file=sys.stderr)
    return selected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Path to the .txt word list")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--words-output", type=Path, default=EVAL_DIR / "eval_words.json")
    parser.add_argument("--gold-output", type=Path, default=EVAL_DIR / "gold.json")
    return parser.parse_args()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    words = [word for word in load_words(args.input) if word not in FEW_SHOT_WORDS]
    random.Random(args.seed).shuffle(words)

    gold = collect(words, DEFAULT_QUOTAS)
    eval_words = [{"word": item["query"], "context": spelling_hint(item["query"])} for item in gold]
    write_json(args.gold_output, gold)
    write_json(args.words_output, eval_words)
    print(f"Wrote {len(gold)} gold entries to {args.gold_output}")


if __name__ == "__main__":
    main()

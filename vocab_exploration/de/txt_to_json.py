#!/usr/bin/env python3
"""Convert a German word list (.txt, one word/phrase per line) to meta_generator input.

Each entry gets a spelling hint as `context`; the model decides the real POS.
"""

import argparse
import json
import random
import re
from pathlib import Path

FEW_SHOT_WORDS = frozenset({"Verkehr", "fahren", "anrufen", "freundlich", "Bescheid geben"})


def normalize(line: str) -> str:
    """Collapse whitespace and trailing ellipses ("je ... desto ..." → "je ... desto")."""
    line = re.sub(r"\s+", " ", line).strip()
    return re.sub(r"(\s*\.\.\.)+$", "", line)


def spelling_hint(word: str) -> str:
    case = "capitalized" if word[0].isupper() else "lowercase"
    return f"multi-word, {case}" if " " in word else case


def load_words(path: Path) -> list[str]:
    """Read, normalize and dedupe words, keeping file order."""
    words = (normalize(line) for line in path.read_text(encoding="utf-8").splitlines())
    return list(dict.fromkeys(word for word in words if word))


def to_entries(words: list[str]) -> list[dict[str, str]]:
    return [{"word": word, "context": spelling_hint(word)} for word in words]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Path to the .txt word list")
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--sample", type=int, help="Random subsample size")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--keep-few-shot",
        action="store_true",
        help="Keep words that appear as few-shot examples in prompt.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    words = load_words(args.input)
    if not args.keep_few_shot:
        words = [word for word in words if word not in FEW_SHOT_WORDS]
    if args.sample:
        words = random.Random(args.seed).sample(words, args.sample)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(to_entries(words), indent=2, ensure_ascii=False)
    args.output.write_text(payload + "\n", encoding="utf-8")
    print(f"Wrote {len(words)} entries to {args.output}")


if __name__ == "__main__":
    main()

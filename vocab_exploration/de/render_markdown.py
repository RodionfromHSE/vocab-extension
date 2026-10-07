#!/usr/bin/env python3
"""Render enriched German entries (meta_generator output) as a readable Markdown page."""

import argparse
import json
from pathlib import Path
from typing import Any

from formatting import grammar_line, grammar_tags, headword


def overview_table(entries: list[dict[str, Any]]) -> str:
    lines = ["| # | Wort | Grammatik | English |", "|---|---|---|---|"]
    for index, entry in enumerate(entries, 1):
        lines.append(
            f"| {index} | [**{headword(entry)}**](#{index}) | {grammar_line(entry) or '—'} | {entry['word_en']} |"
        )
    return "\n".join(lines)


def examples_table(examples: list[dict[str, str]]) -> str:
    lines = ["| Deutsch | English |", "|---|---|"]
    lines += [f"| {example['de']} | *{example['en']}* |" for example in examples]
    return "\n".join(lines)


def entry_section(index: int, entry: dict[str, Any]) -> str:
    tags = " · ".join(f"`{tag}`" for tag in grammar_tags(entry))
    grammar = grammar_line(entry, with_genitive=True)
    lines = [
        f'<a id="{index}"></a>',
        f"### {index}. {headword(entry)}",
        "",
        f"{tags}" + (f" &nbsp;·&nbsp; **{grammar}**" if grammar else ""),
        "",
        f"**→ {entry['word_en']}**",
        "",
        f"> 🇩🇪 {entry['definition_de']}  ",
        f"> 🇬🇧 {entry['definition_en']}",
        "",
        examples_table(entry["examples"]),
    ]
    return "\n".join(lines)


def render(entries: list[dict[str, Any]], title: str) -> str:
    sections = [
        f"# {title}",
        f"{len(entries)} words",
        overview_table(entries),
        "---",
        "\n\n---\n\n".join(entry_section(index, entry) for index, entry in enumerate(entries, 1)),
    ]
    return "\n\n".join(sections) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Enriched JSON (list of entries)")
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--title", default="German vocabulary")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    entries = [entry for entry in json.loads(args.input.read_text(encoding="utf-8")) if "error" not in entry]
    args.output.write_text(render(entries, args.title), encoding="utf-8")
    print(f"Wrote {len(entries)} entries to {args.output}")


if __name__ == "__main__":
    main()

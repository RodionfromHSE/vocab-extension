#!/usr/bin/env python3
"""Score bake-off results against Cambridge gold + blind judges; write report.md.

Grammar is checked deterministically, and only on fields Cambridge provides
(it lists irregular verb forms only). Judge scores exclude self-judgments.
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

EVAL_DIR = Path(__file__).resolve().parent
ARTICLE_TOKENS = {"der", "die", "das", "des", "dem", "den"}
JUDGE_BOOL_KEYS = (
    "sense_matches_cambridge",
    "sense_is_most_common",
    "word_en_ok",
    "definitions_ok",
    "translations_ok",
)
FULL_LIST_SIZE = 2962


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def strip_article(text: str) -> str:
    words = text.strip().split()
    while words and words[0].lower() in ARTICLE_TOKENS:
        words = words[1:]
    return " ".join(words)


def genitive_stem(text: str) -> str:
    """Treat 'Lebenslaufes' and 'Lebenslaufs' as the same genitive."""
    word = strip_article(text)
    for suffix in ("es", "s"):
        if word.endswith(suffix):
            return word.removesuffix(suffix)
    return word


def any_variant_matches(model_value: str, gold_value: str, normalize) -> bool:
    variants = [v for v in model_value.replace(",", "/").split("/") if v.strip()]
    return any(normalize(v) == normalize(gold_value) for v in variants)


def expected_pos(bucket: str) -> set[str] | None:
    return {
        "noun": {"noun"},
        "verb": {"verb"},
        "adjective_adverb": {"adjective", "adverb"},
    }.get(bucket)


def grammar_checks(gold: dict[str, Any], output: dict[str, Any]) -> dict[str, bool]:
    """Exact-match checks on the grammar fields Cambridge provides."""
    checks: dict[str, bool] = {}
    if allowed := expected_pos(gold["bucket"]):
        checks["pos"] = output["pos"] in allowed
    if gold["bucket"] == "noun":
        checks["article"] = output["article"] == gold["article"]
        if gold["plural"]:
            checks["plural"] = any_variant_matches(output["plural"], gold["plural"], strip_article)
        elif gold["uncountable"]:
            checks["plural"] = output["plural"] == ""
        if gold["genitive"]:
            checks["genitive"] = any_variant_matches(output["genitive"], gold["genitive"], genitive_stem)
    if gold["bucket"] == "verb":
        for key in ("praesens_3sg", "praeteritum", "partizip_2"):
            if gold[key]:
                checks[key] = strip_article(output[key]) == gold[key]
        checks["auxiliary"] = output["auxiliary"] == ("sein" if gold["perfekt_mit_sein"] else "haben")
    return checks


def judge_scores_for(judgments: dict[str, Any], model: str, index: int) -> list[dict[str, Any]]:
    """All judgments of `model` on word `index`, excluding the model judging itself."""
    return [
        {**data["scores"][index][model], "judge": judge}
        for judge, data in judgments["judges"].items()
        if judge != model and model in data["scores"][index]
    ]


def summarize_model(
    model: str, rows: list[dict[str, Any]], gold: list[dict[str, Any]], judgments: dict[str, Any]
) -> dict[str, Any]:
    grammar_total, grammar_ok = 0, 0
    judge_rows = []
    for index, (row, gold_entry) in enumerate(zip(rows, gold)):
        if row["output"] is None:
            continue
        checks = grammar_checks(gold_entry, row["output"])
        grammar_total += len(checks)
        grammar_ok += sum(checks.values())
        judge_rows += judge_scores_for(judgments, model, index)

    valid = [row for row in rows if row["output"] is not None]
    cost_per_word = mean(row["cost_usd"] for row in rows)
    summary = {
        "model": model,
        "valid": f"{len(valid)}/{len(rows)}",
        "retries": sum(row["calls"] - 1 for row in rows),
        "grammar_acc": grammar_ok / grammar_total if grammar_total else 0.0,
        "grammar_checked": grammar_total,
        "naturalness": mean(j["examples_naturalness"] for j in judge_rows),
        "judge_grammar_clean": mean(not j["grammar_errors"] for j in judge_rows),
        "latency": mean(row["latency_seconds"] for row in rows),
        "cost_per_word": cost_per_word,
        "projected_cost": cost_per_word * FULL_LIST_SIZE,
    }
    for key in JUDGE_BOOL_KEYS:
        summary[key] = mean(bool(j[key]) for j in judge_rows)
    return summary


def pct(value: float) -> str:
    return f"{value * 100:.0f}%"


def summary_table(summaries: list[dict[str, Any]]) -> str:
    header = (
        "| model | valid | retries | grammar vs Cambridge | sense = Cambridge #1 | most common sense "
        "| word_en ok | definitions ok | translations ok | judge: no grammar errors | naturalness (1–5) "
        "| latency | $/word | $ for full list |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"
    )
    lines = [header]
    for s in summaries:
        lines.append(
            f"| **{s['model']}** | {s['valid']} | {s['retries']} | {pct(s['grammar_acc'])} ({s['grammar_checked']} checks) "
            f"| {pct(s['sense_matches_cambridge'])} | {pct(s['sense_is_most_common'])} | {pct(s['word_en_ok'])} "
            f"| {pct(s['definitions_ok'])} | {pct(s['translations_ok'])} | {pct(s['judge_grammar_clean'])} "
            f"| {s['naturalness']:.2f} | {s['latency']:.1f}s | ${s['cost_per_word']:.4f} | ${s['projected_cost']:.2f} |"
        )
    return "\n".join(lines)


def grammar_line(entry: dict[str, Any]) -> str:
    """Compact one-line grammar summary for a model output."""
    if entry["pos"] == "noun":
        return f"{entry['article']} · pl. {entry['plural'] or '—'} · gen. {entry['genitive'] or '—'}"
    if entry["perfekt"]:
        flags = " ".join(f for f, on in (("trennbar", entry["separable"]), ("refl.", entry["reflexive"])) if on)
        forms = f"{entry['praesens_3sg']} · {entry['praeteritum']} · {entry['perfekt']}"
        return f"{forms} {flags}".strip()
    if entry["comparative"]:
        return f"{entry['comparative']} · {entry['superlative']}"
    return entry["pos"]


def gold_grammar_line(gold: dict[str, Any]) -> str:
    if gold["bucket"] == "noun":
        return f"{gold['article']} · pl. {gold['plural'] or '—'} · gen. {gold['genitive'] or '—'}"
    if gold["bucket"] == "verb":
        aux = "sein" if gold["perfekt_mit_sein"] else "haben"
        forms = " · ".join(f for f in (gold["praesens_3sg"], gold["praeteritum"], gold["partizip_2"]) if f)
        return f"{forms or '(regular)'} · {aux}"
    return gold["pos"]


def cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def format_examples(examples: list[dict[str, str]]) -> str:
    return "<br>".join(f"{e['de']} — *{e['en']}*" if e["en"] else e["de"] for e in examples[:2])


def word_section(index: int, gold: dict[str, Any], results: dict[str, list], judgments: dict[str, Any]) -> str:
    lines = [
        f"### {index + 1}. {gold['query']} ({gold['bucket']})",
        "",
        "| source | grammar | word_en | definition_de | examples | failed checks |",
        "|---|---|---|---|---|---|",
        f"| Cambridge | {cell(gold_grammar_line(gold))} | {cell(', '.join(gold['translations_en']))} "
        f"| {cell(gold['definition_de'])} | {cell(format_examples(gold['examples']))} | |",
    ]
    comments = []
    for model, rows in results.items():
        output = rows[index]["output"]
        if output is None:
            lines.append(f"| {model} | ❌ {cell(rows[index]['error'] or '')} | | | | |")
            continue
        failed = [key for key, ok in grammar_checks(gold, output).items() if not ok]
        lines.append(
            f"| {model} | {cell(grammar_line(output))} | {cell(output['word_en'])} | {cell(output['definition_de'])} "
            f"| {cell(format_examples(output['examples']))} | {', '.join(failed)} |"
        )
        for judged in judge_scores_for(judgments, model, index):
            issues = [judged["comment"], *judged["grammar_errors"]]
            issues = [issue for issue in issues if issue]
            if issues:
                comments.append(f"- **{model}** (judge {judged['judge']}): {'; '.join(issues)}")
    return "\n".join(lines + ([""] + comments if comments else []))


def build_report(gold: list, results: dict[str, list], judgments: dict[str, Any], summaries: list) -> str:
    judge_cost = sum(data["cost_usd"] for data in judgments["judges"].values())
    sections = [
        "# German vocab generation: model bake-off",
        f"{len(gold)} words (stratified: nouns, verbs, adjectives/adverbs, phrases), none of them few-shot examples. "
        "Grammar is checked against Cambridge GLOBAL German–English, only on the fields Cambridge lists. "
        "Semantic scores come from blind cross-model judges (each output is rated by the two *other* models; "
        f"judging cost ${judge_cost:.2f}).",
        "## Summary",
        summary_table(summaries),
        "## Per word",
        *(word_section(index, entry, results, judgments) for index, entry in enumerate(gold)),
    ]
    return "\n\n".join(sections) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold", type=Path, default=EVAL_DIR / "gold.json")
    parser.add_argument("--results-dir", type=Path, default=EVAL_DIR / "results")
    parser.add_argument("--judgments", type=Path, default=EVAL_DIR / "judgments.json")
    parser.add_argument("--output", type=Path, default=EVAL_DIR / "report.md")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    gold = load_json(args.gold)
    judgments = load_json(args.judgments)
    results = {
        path.stem: load_json(path)["results"] for path in sorted(args.results_dir.glob("*.json"))
    }
    summaries = [summarize_model(model, rows, gold, judgments) for model, rows in results.items()]
    args.output.write_text(build_report(gold, results, judgments, summaries), encoding="utf-8")
    print(summary_table(summaries))
    print(f"\nWrote {args.output}")


if __name__ == "__main__":
    main()

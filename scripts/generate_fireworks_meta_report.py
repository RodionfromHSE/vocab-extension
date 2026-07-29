#!/usr/bin/env python3
"""Generate a Kimi K3 meta-only quality and cost report."""

import argparse
import json
import os
import random
import sys
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
META_ROOT = ROOT / "meta_generator"
sys.path.insert(0, str(META_ROOT))

from main import create_components
from src.model.fireworks_model import FireworksModel, TokenUsage
from src.utils.config import read_config


@dataclass(frozen=True)
class KimiK3Pricing:
    """Current Fireworks serverless prices in USD per million tokens."""

    input_per_million: float = 3.0
    cached_input_per_million: float = 0.3
    output_per_million: float = 15.0

    def calculate(self, usage: TokenUsage) -> float:
        """Calculate request cost from uncached, cached, and output tokens."""
        uncached = usage.prompt_tokens - usage.cached_prompt_tokens
        total = uncached * self.input_per_million
        total += usage.cached_prompt_tokens * self.cached_input_per_million
        total += usage.completion_tokens * self.output_per_million
        return total / 1_000_000


@dataclass(frozen=True)
class GenerationRecord:
    """One input/output pair with usage and cost."""

    input: dict[str, Any]
    reasoning_effort: str
    output: dict[str, Any] | str
    usage: TokenUsage
    cost_usd: float


def parse_args() -> argparse.Namespace:
    """Parse report options."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=META_ROOT / "config.yaml")
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--sample-size", type=int, default=5)
    parser.add_argument("--reasoning-effort", choices=("low", "medium"), default="low")
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-markdown", type=Path, required=True)
    return parser.parse_args()


def load_entries(input_dir: Path) -> list[dict[str, Any]]:
    """Load top-level Word Saver entries."""
    paths = sorted(input_dir.glob("*.json"))
    if not paths:
        raise ValueError(f"No JSON inputs found in {input_dir}")
    return [json.loads(path.read_text(encoding="utf-8")) for path in paths]


def generate_record(
    handler: Any,
    model: FireworksModel,
    entry: dict[str, Any],
    effort: str,
    pricing: KimiK3Pricing,
) -> GenerationRecord:
    """Generate and price one metadata response."""
    output = handler.handle(entry, reasoning_effort=effort)
    if model.last_usage is None:
        raise RuntimeError("Fireworks did not return token usage")
    return GenerationRecord(
        entry, effort, output, model.last_usage, pricing.calculate(model.last_usage)
    )


def record_to_dict(record: GenerationRecord) -> dict[str, Any]:
    """Serialize a generation record."""
    payload = asdict(record)
    payload["cost_usd"] = round(record.cost_usd, 8)
    return payload


def format_record(record: GenerationRecord) -> str:
    """Format one record as Markdown."""
    input_json = json.dumps(record.input, indent=2, ensure_ascii=False)
    output_json = json.dumps(record.output, indent=2, ensure_ascii=False)
    usage = record.usage
    return (
        f"Reasoning: `{record.reasoning_effort}` · "
        f"tokens: `{usage.prompt_tokens}` input / `{usage.completion_tokens}` output "
        f"(`{usage.cached_prompt_tokens}` cached) · cost: `${record.cost_usd:.6f}`\n\n"
        f"Input:\n\n```json\n{input_json}\n```\n\n"
        f"Output:\n\n```json\n{output_json}\n```"
    )


def build_markdown(
    report: dict[str, Any],
    comparisons: list[GenerationRecord],
    samples: list[GenerationRecord],
) -> str:
    """Render the complete report."""
    total = sum(item.cost_usd for item in samples)
    sections = [
        "# Fireworks Kimi K3 meta-generator report",
        f"Generated: `{report['generated_at']}`",
        "Model: `accounts/fireworks/models/kimi-k3`",
        "Pricing: $3/M input, $0.30/M cached input, $15/M output.",
        "## Reasoning comparison (same input)",
    ]
    sections.extend(
        f"### {item.reasoning_effort.title()}\n\n{format_record(item)}"
        for item in comparisons
    )
    sections.append(f"## Five-word sample (`{report['selected_reasoning_effort']}`)")
    sections.extend(
        f"### {index}. {item.input.get('word', 'Unknown')}\n\n{format_record(item)}"
        for index, item in enumerate(samples, 1)
    )
    sections.append(
        f"## Sample cost summary\n\nTotal: `${total:.6f}` · "
        f"average per word: `${total / len(samples):.6f}`"
    )
    return "\n\n".join(sections) + "\n"


def generate_samples(
    handler: Any,
    model: FireworksModel,
    entries: list[dict[str, Any]],
    effort: str,
    comparisons: list[GenerationRecord],
    pricing: KimiK3Pricing,
) -> list[GenerationRecord]:
    """Generate the selected-effort sample while reusing its comparison call."""
    comparison_by_effort = {item.reasoning_effort: item for item in comparisons}
    return [
        comparison_by_effort[effort]
        if index == 0
        else generate_record(handler, model, entry, effort, pricing)
        for index, entry in enumerate(entries)
    ]


def write_reports(
    args: argparse.Namespace,
    report: dict[str, Any],
    comparisons: list[GenerationRecord],
    samples: list[GenerationRecord],
) -> None:
    """Write machine-readable and human-readable reports."""
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_markdown.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    args.output_markdown.write_text(
        build_markdown(report, comparisons, samples),
        encoding="utf-8",
    )


def main() -> None:
    """Generate JSON and Markdown reports."""
    args = parse_args()
    input_dir = args.input_dir or Path(os.environ["WORD_SAVER_SAVE_DIRECTORY"])
    selected = random.SystemRandom().sample(load_entries(input_dir), args.sample_size)
    config = read_config(str(args.config))
    config["prompt_path"] = str((args.config.parent / config["prompt_path"]).resolve())
    model, _, _, _, handler = create_components(config)
    if not isinstance(model, FireworksModel):
        raise TypeError("Report requires api.type=fireworks")

    pricing = KimiK3Pricing()
    comparisons = [
        generate_record(handler, model, selected[0], effort, pricing)
        for effort in ("low", "medium", "high")
    ]
    samples = generate_samples(
        handler,
        model,
        selected,
        args.reasoning_effort,
        comparisons,
        pricing,
    )
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "model": model.generation_params["model"],
        "selected_reasoning_effort": args.reasoning_effort,
        "pricing_usd_per_million_tokens": asdict(pricing),
        "reasoning_comparison": [record_to_dict(item) for item in comparisons],
        "sample_results": [record_to_dict(item) for item in samples],
    }
    write_reports(args, report, comparisons, samples)


if __name__ == "__main__":
    main()

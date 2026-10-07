#!/usr/bin/env python3
"""Run the German prompt on the eval words with several Fireworks models.

Each model runs in its own thread (words sequentially), so per-word latency is
realistic. Writes `results/<model>.json` with output, usage, cost and latency.
"""

import argparse
import copy
import json
import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

EVAL_DIR = Path(__file__).resolve().parent
DE_DIR = EVAL_DIR.parent
META_ROOT = DE_DIR.parent.parent / "meta_generator"
sys.path.insert(0, str(META_ROOT))

from main import create_components
from src.handler.generation_handler import GenerationHandler
from src.model.base_model import BaseModel
from src.model.fireworks_model import FireworksModel
from src.utils.config import read_config


@dataclass(frozen=True)
class Pricing:
    """Fireworks serverless (Standard) prices in USD per million tokens."""

    input_per_million: float
    cached_input_per_million: float
    output_per_million: float


@dataclass(frozen=True)
class ModelSpec:
    name: str
    model_id: str
    pricing: Pricing
    reasoning_effort: str | None = "low"


MODELS = {
    "kimi-k3": ModelSpec(
        "kimi-k3", "accounts/fireworks/models/kimi-k3", Pricing(3.0, 0.3, 15.0)
    ),
    "glm-5p3": ModelSpec(
        "glm-5p3", "accounts/fireworks/models/glm-5p3", Pricing(1.4, 0.26, 4.4)
    ),
    "deepseek-v4p1-flash": ModelSpec(
        "deepseek-v4p1-flash",
        "accounts/fireworks/models/deepseek-v4p1-flash",
        Pricing(0.3, 0.006, 1.2),
    ),
}


@dataclass
class UsageTotals:
    calls: int = 0
    prompt_tokens: int = 0
    cached_prompt_tokens: int = 0
    completion_tokens: int = 0

    def cost(self, pricing: Pricing) -> float:
        uncached = self.prompt_tokens - self.cached_prompt_tokens
        total = uncached * pricing.input_per_million
        total += self.cached_prompt_tokens * pricing.cached_input_per_million
        total += self.completion_tokens * pricing.output_per_million
        return total / 1_000_000


class MeteredModel(BaseModel):
    """Wrap a FireworksModel to count every call, including handler retries."""

    def __init__(self, inner: FireworksModel):
        super().__init__(inner.config)
        self.inner = inner
        self.totals = UsageTotals()

    def reset(self) -> None:
        self.totals = UsageTotals()

    def validate_config(self) -> bool:
        return self.inner.validate_config()

    def generate(self, prompt: str, **kwargs: Any) -> str:
        self.totals.calls += 1
        try:
            return self.inner.generate(prompt, **kwargs)
        finally:
            usage = self.inner.last_usage
            if usage is not None:
                self.totals.prompt_tokens += usage.prompt_tokens
                self.totals.cached_prompt_tokens += usage.cached_prompt_tokens
                self.totals.completion_tokens += usage.completion_tokens
            self.inner.last_usage = None


@dataclass
class WordResult:
    input: dict[str, Any]
    output: dict[str, Any] | None
    error: str | None
    latency_seconds: float
    usage: UsageTotals
    cost_usd: float
    calls: int = field(init=False)

    def __post_init__(self) -> None:
        self.calls = self.usage.calls


def build_handler(base_config: Any, spec: ModelSpec) -> tuple[GenerationHandler, MeteredModel]:
    config = copy.deepcopy(base_config)
    config.api.model = spec.model_id
    config.api.params.reasoning_effort = spec.reasoning_effort
    model, prompter, processor, validator, _ = create_components(config)
    metered = MeteredModel(model)
    return GenerationHandler(config, metered, prompter, processor, validator), metered


def run_word(
    handler: GenerationHandler, metered: MeteredModel, entry: dict[str, Any], spec: ModelSpec
) -> WordResult:
    metered.reset()
    started = time.perf_counter()
    output, error = None, None
    try:
        output = handler.handle(entry)
    except Exception as exc:  # keep going; failures are part of the comparison
        error = f"{type(exc).__name__}: {exc}"
    latency = time.perf_counter() - started
    totals = metered.totals
    return WordResult(entry, output, error, round(latency, 2), totals, totals.cost(spec.pricing))


def run_model(base_config: Any, spec: ModelSpec, entries: list[dict[str, Any]], out_dir: Path) -> Path:
    handler, metered = build_handler(base_config, spec)
    results = []
    for index, entry in enumerate(entries, 1):
        result = run_word(handler, metered, entry, spec)
        status = "ERR" if result.error else "ok"
        print(f"[{spec.name}] {index}/{len(entries)} {entry['word']}: {status} {result.latency_seconds}s")
        results.append(asdict(result))

    payload = {"model": spec.name, "model_id": spec.model_id, "pricing": asdict(spec.pricing), "results": results}
    path = out_dir / f"{spec.name}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DE_DIR / "config.yaml")
    parser.add_argument("--words", type=Path, default=EVAL_DIR / "eval_words.json")
    parser.add_argument("--out-dir", type=Path, default=EVAL_DIR / "results")
    parser.add_argument("--models", nargs="+", choices=sorted(MODELS), default=list(MODELS))
    parser.add_argument("--limit", type=int, help="Only the first N words (for quick checks)")
    return parser.parse_args()


def main() -> None:
    logging.getLogger().setLevel(logging.CRITICAL)  # handler logs every retry; we report errors ourselves
    args = parse_args()
    entries = json.loads(args.words.read_text(encoding="utf-8"))[: args.limit]
    base_config = read_config(str(args.config))
    args.out_dir.mkdir(parents=True, exist_ok=True)

    specs = [MODELS[name] for name in args.models]
    with ThreadPoolExecutor(max_workers=len(specs)) as pool:
        futures = [pool.submit(run_model, base_config, spec, entries, args.out_dir) for spec in specs]
        for future in futures:
            print(f"Wrote {future.result()}")


if __name__ == "__main__":
    main()

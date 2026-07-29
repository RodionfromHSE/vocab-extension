"""Fireworks AI model adapter."""

import logging
import os
from dataclasses import dataclass
from typing import Any

from fireworks import Fireworks
from omegaconf import DictConfig

from src.model.base_model import BaseModel

logger = logging.getLogger(__name__)
REASONING_EFFORTS = frozenset({"low", "medium", "high"})
DEFAULT_PARAMS = {
    "model": "accounts/fireworks/models/kimi-k3",
    "max_tokens": 4096,
    "temperature": 0.2,
    "timeout": 120,
    "reasoning_effort": "low",
}


@dataclass(frozen=True)
class TokenUsage:
    """Token usage from the most recent generation."""

    prompt_tokens: int
    completion_tokens: int
    cached_prompt_tokens: int


class FireworksModel(BaseModel):
    """Generate text with the native Fireworks Python SDK."""

    def __init__(self, config: dict[str, Any] | DictConfig):
        super().__init__(config)
        self.client = self._setup_client()
        self.generation_params = self._initialize_generation_params()
        self.last_usage: TokenUsage | None = None

    def _setup_client(self) -> Fireworks:
        api_config = self.config.get("api", {})
        api_key = api_config.get("key") or os.environ.get("FIREWORKS_API_KEY")
        if not api_key:
            raise ValueError(
                "Fireworks API key not provided in config or FIREWORKS_API_KEY"
            )

        return Fireworks(
            api_key=api_key,
            base_url=api_config.get("base_url"),
            max_retries=api_config.get("max_retries", 2),
        )

    def _initialize_generation_params(self) -> dict[str, Any]:
        api_config = self.config.get("api", {})
        configured_params = api_config.get("params", {})
        params = {
            **DEFAULT_PARAMS,
            **configured_params,
            "model": api_config.get("model", DEFAULT_PARAMS["model"]),
        }
        self._validate_reasoning_effort(params["reasoning_effort"])
        return params

    @staticmethod
    def _validate_reasoning_effort(reasoning_effort: str | None) -> None:
        if reasoning_effort is not None and reasoning_effort not in REASONING_EFFORTS:
            allowed = ", ".join(sorted(REASONING_EFFORTS))
            raise ValueError(f"reasoning_effort must be one of: {allowed}")

    def validate_config(self) -> bool:
        """Return whether the SDK client and model ID are configured."""
        return bool(self.client and self.generation_params["model"])

    def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate text and retain token usage for cost reporting."""
        if not self.validate_config():
            raise ValueError("Invalid configuration for FireworksModel")

        payload = self._build_payload(prompt, kwargs)
        try:
            response = self.client.chat.completions.create(**payload)
            self.last_usage = self._extract_usage(response.usage)
            content = response.choices[0].message.content
            if not content:
                finish_reason = response.choices[0].finish_reason
                raise ValueError(
                    f"Empty Fireworks response (finish_reason={finish_reason})"
                )
            return content.strip()
        except Exception:
            logger.exception("Fireworks API generation failed")
            raise

    def _build_payload(self, prompt: str, overrides: dict[str, Any]) -> dict[str, Any]:
        reasoning_effort = overrides.get(
            "reasoning_effort", self.generation_params["reasoning_effort"]
        )
        self._validate_reasoning_effort(reasoning_effort)
        payload = {
            "model": self.generation_params["model"],
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": overrides.get(
                "max_tokens", self.generation_params["max_tokens"]
            ),
            "temperature": overrides.get(
                "temperature", self.generation_params["temperature"]
            ),
            "timeout": overrides.get("timeout", self.generation_params["timeout"]),
        }
        if reasoning_effort is not None:
            payload["reasoning_effort"] = reasoning_effort
        return payload

    @staticmethod
    def _extract_usage(usage: Any) -> TokenUsage | None:
        if usage is None:
            return None
        details = usage.prompt_tokens_details
        cached_tokens = details.cached_tokens if details else 0
        return TokenUsage(
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens or 0,
            cached_prompt_tokens=cached_tokens or 0,
        )

"""Tests for the native Fireworks model adapter."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from src.model.fireworks_model import FireworksModel, TokenUsage


def make_config(reasoning_effort: str = "low") -> dict:
    """Build a minimal Fireworks test configuration."""
    return {
        "api": {
            "key": "test-key",
            "model": "accounts/fireworks/models/kimi-k3",
            "params": {
                "max_tokens": 512,
                "temperature": 0.2,
                "timeout": 30,
                "reasoning_effort": reasoning_effort,
            },
        }
    }


def make_response(content: str = "result") -> SimpleNamespace:
    """Build a Fireworks-shaped completion response."""
    usage = SimpleNamespace(
        prompt_tokens=100,
        completion_tokens=25,
        prompt_tokens_details=SimpleNamespace(cached_tokens=10),
    )
    message = SimpleNamespace(content=content)
    choice = SimpleNamespace(message=message, finish_reason="stop")
    return SimpleNamespace(choices=[choice], usage=usage)


@patch("src.model.fireworks_model.Fireworks")
def test_generate_passes_reasoning_and_records_usage(mock_fireworks: MagicMock) -> None:
    """Pass Kimi reasoning effort and retain billable token usage."""
    mock_fireworks.return_value.chat.completions.create.return_value = make_response()
    model = FireworksModel(make_config())

    assert model.generate("prompt") == "result"
    assert model.last_usage == TokenUsage(100, 25, 10)
    mock_fireworks.return_value.chat.completions.create.assert_called_once_with(
        model="accounts/fireworks/models/kimi-k3",
        messages=[{"role": "user", "content": "prompt"}],
        max_tokens=512,
        temperature=0.2,
        timeout=30,
        reasoning_effort="low",
    )


@patch("src.model.fireworks_model.Fireworks")
def test_generate_accepts_reasoning_override(mock_fireworks: MagicMock) -> None:
    """Allow low, medium, or high reasoning per generation."""
    mock_fireworks.return_value.chat.completions.create.return_value = make_response()
    model = FireworksModel(make_config())

    model.generate("prompt", reasoning_effort="high")

    payload = mock_fireworks.return_value.chat.completions.create.call_args.kwargs
    assert payload["reasoning_effort"] == "high"


@patch("src.model.fireworks_model.Fireworks")
def test_rejects_invalid_reasoning_effort(mock_fireworks: MagicMock) -> None:
    """Reject unsupported reasoning effort before making a request."""
    with pytest.raises(ValueError, match="reasoning_effort"):
        FireworksModel(make_config("extreme"))

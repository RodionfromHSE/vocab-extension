"""Tests for the Nebius OpenAI-compatible model adapter."""

from typing import Any
from unittest.mock import MagicMock, patch

from src.model.nebius_model import NebiusModel


def make_config(reasoning_effort: str | None = "low") -> dict[str, Any]:
    """Build a minimal Nebius test configuration."""
    params = {
        "max_tokens": 512,
        "temperature": 0.2,
        "timeout": 30,
    }
    if reasoning_effort is not None:
        params["reasoning_effort"] = reasoning_effort
    return {
        "api": {
            "key": "test-key",
            "model": "moonshotai/Kimi-K3",
            "base_url": "https://api.studio.nebius.ai/v1",
            "params": params,
        }
    }


@patch("src.model.nebius_model.OpenAI")
def test_generate_passes_configured_reasoning_effort(mock_openai: MagicMock) -> None:
    """Pass configured reasoning effort to Nebius chat completions."""
    response = MagicMock()
    response.choices[0].message.content = "result"
    mock_openai.return_value.chat.completions.create.return_value = response

    model = NebiusModel(make_config())

    assert model.generate("prompt") == "result"
    mock_openai.return_value.chat.completions.create.assert_called_once_with(
        model="moonshotai/Kimi-K3",
        messages=[{"role": "user", "content": "prompt"}],
        max_tokens=512,
        temperature=0.2,
        timeout=30,
        reasoning_effort="low",
    )


@patch("src.model.nebius_model.OpenAI")
def test_generate_omits_unconfigured_reasoning_effort(mock_openai: MagicMock) -> None:
    """Keep reasoning optional for non-reasoning models."""
    response = MagicMock()
    response.choices[0].message.content = "result"
    mock_openai.return_value.chat.completions.create.return_value = response

    model = NebiusModel(make_config(reasoning_effort=None))
    model.generate("prompt")

    call_payload = mock_openai.return_value.chat.completions.create.call_args.kwargs
    assert "reasoning_effort" not in call_payload

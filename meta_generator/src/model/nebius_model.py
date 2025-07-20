# src/model/nebius_model.py
import os
import logging
from typing import Dict, Any
from openai import OpenAI

from src.model.base_model import BaseModel

# Re-use DEFAULT_PARAMS from your module
DEFAULT_PARAMS = {
    "model": "deepseek-ai/DeepSeek-V3-0324",  # Nebius model slug
    "max_tokens": 1000,
    "temperature": 0.7,
    "timeout": 30,
}

class NebiusModel(BaseModel):
    """
    Nebius AI Studio client that uses the OpenAI-compatible /v1/chat/completions
    endpoint to run DeepSeek-V3-0324 (or any other Nebius model).
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = self._setup_client()
        self.generation_params = self._init_generation_params()

    # ---------- internal helpers ----------
    def _setup_client(self) -> OpenAI:
        api_key = (
            self.config.get("api", {}).get("key")
            or os.getenv("NEBIUS_API_KEY")           # recommended env var
        )
        if not api_key:
            raise ValueError("Nebius API key not provided")

        base_url = self.config.get("api", {}).get(
            "base_url", "https://api.studio.nebius.ai/v1"
        )
        # Nebius is wire-compatible with the OpenAI SDK
        return OpenAI(api_key=api_key, base_url=base_url)

    def _init_generation_params(self) -> Dict[str, Any]:
        params = DEFAULT_PARAMS.copy()
        api_cfg   = self.config.get("api", {})
        api_param = api_cfg.get("params", {})

        params["model"]       = api_cfg.get("model", params["model"])
        params["max_tokens"]  = api_param.get("max_tokens", params["max_tokens"])
        params["temperature"] = api_param.get("temperature", params["temperature"])
        params["timeout"]     = api_param.get("timeout", params["timeout"])
        return params

    # ---------- BaseModel interface ----------
    def validate_config(self) -> bool:
        return bool(self.client and self.generation_params["model"])

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.validate_config():
            raise ValueError("Invalid configuration for NebiusModel")

        try:
            messages = [{"role": "user", "content": prompt}]
            # Merge any ad-hoc overrides the caller passed via **kwargs
            payload = {
                "model": self.generation_params["model"],
                "messages": messages,
                "max_tokens": kwargs.get("max_tokens", self.generation_params["max_tokens"]),
                "temperature": kwargs.get("temperature", self.generation_params["temperature"]),
                "timeout": kwargs.get("timeout", self.generation_params["timeout"]),
            }

            resp = self.client.chat.completions.create(**payload)
            return resp.choices[0].message.content.strip()

        except Exception as err:
            logging.error("Nebius API error: %s", err)
            raise

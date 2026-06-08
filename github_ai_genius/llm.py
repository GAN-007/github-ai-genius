from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from .config import Settings

SYSTEM_PROMPT = """You are GitHub AI Genius, a local-first senior engineering agent.
Produce complete, working, production-grade code. Do not emit fake files, placeholders, TODOs, or hypothetical structures.
Respect software licenses, preserve attribution where required, and create original clean-room implementations when direct reuse is not appropriate.
Assist with defensive engineering, secure coding, authorized testing, refactoring, design, DevOps, and application delivery.
"""


@dataclass(slots=True)
class OllamaClient:
    settings: Settings

    async def generate(self, prompt: str, system: str = SYSTEM_PROMPT, temperature: float = 0.15) -> str:
        payload: dict[str, Any] = {
            "model": self.settings.ollama_model,
            "prompt": prompt,
            "system": system,
            "stream": False,
            "options": {"temperature": temperature, "num_ctx": 32768},
        }
        async with httpx.AsyncClient(timeout=httpx.Timeout(600)) as client:
            response = await client.post(f"{self.settings.ollama_base_url.rstrip('/')}/api/generate", json=payload)
        response.raise_for_status()
        return str(response.json().get("response", "")).strip()

    async def health(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{self.settings.ollama_base_url.rstrip('/')}/api/tags")
        response.raise_for_status()
        return response.json()

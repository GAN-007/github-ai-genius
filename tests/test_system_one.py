from __future__ import annotations

import json

import httpx
import pytest

from github_ai_genius.config import Settings
from github_ai_genius.system_one import GeniusDecisionPlane


@pytest.mark.asyncio
async def test_system_one_disabled_does_not_call_provider():
    async def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("provider must not be called")

    plane = GeniusDecisionPlane(
        Settings(
            GENIUS_SYSTEM_ONE_MODE="off",
            GENIUS_SYSTEM_ONE_BASE_URL="http://laya.test:8000",
        ),
        transport=httpx.MockTransport(handler),
    )
    assert await plane.classify("Analyze owner/repo", explicit_intent="analyze") is None


@pytest.mark.asyncio
async def test_system_one_returns_advisory_task_signals():
    async def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["state"]["explicit_intent"] == "transform"
        assert payload["state"]["policy"]["security_and_license_policy_remain_authoritative"] is True
        return httpx.Response(
            200,
            json={
                "answers": {
                    "domain": {
                        "type": "choice",
                        "choice": "implementation",
                        "confidence": 0.95,
                        "probabilities": {"implementation": 0.95, "other": 0.05},
                    },
                    "high_change_risk": {"type": "noul", "noul": 0.82, "confidence": 0.82},
                },
                "routing": {"model": "english"},
                "usage": {"input_tokens": 61, "output_tokens": 0},
            },
        )

    plane = GeniusDecisionPlane(
        Settings(
            GENIUS_SYSTEM_ONE_MODE="advisory",
            GENIUS_SYSTEM_ONE_BASE_URL="http://laya.test:8000",
            GENIUS_SYSTEM_ONE_API_KEY="test-key",
        ),
        transport=httpx.MockTransport(handler),
    )
    result = await plane.classify(
        "Refactor the repository without breaking existing features",
        explicit_intent="transform",
    )
    assert result is not None
    assert result["advisory_only"] is True
    assert result["answers"]["domain"]["choice"] == "implementation"


@pytest.mark.asyncio
async def test_system_one_provider_failure_fails_open():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, json={"error": "down"})

    plane = GeniusDecisionPlane(
        Settings(
            GENIUS_SYSTEM_ONE_MODE="shadow",
            GENIUS_SYSTEM_ONE_BASE_URL="http://laya.test:8000",
        ),
        transport=httpx.MockTransport(handler),
    )
    assert await plane.classify("Analyze repository", explicit_intent="analyze") is None

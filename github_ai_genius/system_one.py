from __future__ import annotations

import logging
import time
from typing import Any

import httpx

from .config import Settings

logger = logging.getLogger(__name__)


class GeniusDecisionPlane:
    """Fail-open System-One task classifier.

    Security policy and license policy are evaluated by the existing policy
    engine before these advisory signals can influence orchestration.
    """

    def __init__(
        self,
        settings: Settings,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.settings = settings
        self.transport = transport

    @property
    def enabled(self) -> bool:
        return (
            self.settings.system_one_mode in {"shadow", "advisory"}
            and bool(self.settings.system_one_base_url)
        )

    async def classify(self, instruction: str, *, explicit_intent: str) -> dict[str, Any] | None:
        if not self.enabled or not instruction.strip():
            return None

        questions = {
            "domain": {
                "type": "choice",
                "instructions": "Which engineering domain best describes this task?",
                "criteria": {
                    "repository_analysis": "Inspect, audit, understand, compare, or score repositories",
                    "implementation": "Build, modify, refactor, fix, or generate software",
                    "testing_ci": "Tests, CI, build failures, validation, or release gates",
                    "security_review": "Defensive security review, hardening, vulnerability remediation",
                    "architecture": "System design, integration, architecture, or platform planning",
                    "documentation": "Documentation, reports, READMEs, or developer guidance",
                    "other": "None of the listed engineering domains",
                },
            },
            "difficulty": {
                "type": "score",
                "instructions": "How difficult is the engineering task?",
                "criteria": [
                    "small lookup or one-file task",
                    "bounded multi-file task",
                    "multi-component repository work",
                    "complex cross-repository or production-critical work",
                ],
            },
            "needs_repository": {
                "type": "noul",
                "instructions": "Does completing this task require inspecting repository content?",
            },
            "needs_tools": {
                "type": "noul",
                "instructions": "Does completing this task require tools such as GitHub, tests, build commands, or external services?",
            },
            "needs_browser": {
                "type": "noul",
                "instructions": "Does the task materially require browser automation or live web interaction?",
            },
            "high_change_risk": {
                "type": "noul",
                "instructions": "Could an incorrect implementation materially break an existing application or deployment?",
            },
        }
        headers = {"content-type": "application/json"}
        if self.settings.system_one_api_key:
            headers["authorization"] = f"Bearer {self.settings.system_one_api_key}"

        started = time.perf_counter()
        try:
            async with httpx.AsyncClient(
                timeout=self.settings.system_one_timeout_seconds,
                follow_redirects=False,
                transport=self.transport,
            ) as client:
                response = await client.post(
                    f"{self.settings.system_one_base_url.rstrip('/')}/v1/systemone",
                    headers=headers,
                    json={
                        "state": {
                            "instruction": instruction,
                            "explicit_intent": explicit_intent,
                            "policy": {
                                "advisory_only": True,
                                "explicit_task_intent_remains_authoritative": True,
                                "security_and_license_policy_remain_authoritative": True,
                            },
                        },
                        "questions": questions,
                    },
                )
                response.raise_for_status()
                body = response.json()
            answers = body.get("answers")
            if not isinstance(answers, dict):
                raise TypeError("System-One response missing answers")
            return {
                "provider": "laya",
                "mode": self.settings.system_one_mode,
                "advisory_only": True,
                "answers": answers,
                "routing": body.get("routing") if isinstance(body.get("routing"), dict) else None,
                "usage": body.get("usage") if isinstance(body.get("usage"), dict) else None,
                "latency_ms": int((time.perf_counter() - started) * 1000),
            }
        except (httpx.HTTPError, ValueError, TypeError) as exc:
            logger.warning("GitHub AI Genius System-One failed open: %s", exc)
            return None

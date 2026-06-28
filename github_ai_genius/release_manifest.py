from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReleaseCheck:
    name: str
    command: str
    required: bool


DEFAULT_RELEASE_CHECKS: tuple[ReleaseCheck, ...] = (
    ReleaseCheck('unit_tests', 'pytest', True),
    ReleaseCheck('lint', 'ruff check github_ai_genius tests', True),
    ReleaseCheck('type_check', 'mypy github_ai_genius', True),
    ReleaseCheck('container_build', 'docker compose -f compose.yml build', True),
)


def release_checklist() -> list[dict[str, str | bool]]:
    return [{'name': item.name, 'command': item.command, 'required': item.required} for item in DEFAULT_RELEASE_CHECKS]

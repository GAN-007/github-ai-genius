from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class ReleaseResult:
    name: str
    passed: bool
    details: str


@dataclass(frozen=True, slots=True)
class ReleaseReport:
    results: tuple[ReleaseResult, ...]

    @property
    def passed(self) -> bool:
        return all(item.passed for item in self.results)

    @property
    def pass_rate(self) -> int:
        if not self.results:
            return 0
        passed = sum(1 for item in self.results if item.passed)
        return round(passed * 100 / len(self.results))


def load_release_report(path: Path) -> ReleaseReport:
    if not path.exists():
        return ReleaseReport(())
    raw: Any = json.loads(path.read_text(encoding='utf-8'))
    items = raw.get('results', raw if isinstance(raw, list) else [])
    results = tuple(
        ReleaseResult(
            name=str(item.get('name', 'unknown')),
            passed=bool(item.get('passed', False)),
            details=str(item.get('details', '')),
        )
        for item in items
        if isinstance(item, dict)
    )
    return ReleaseReport(results)


def write_release_report(path: Path, report: ReleaseReport) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {'results': [{'name': item.name, 'passed': item.passed, 'details': item.details} for item in report.results]}
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding='utf-8')

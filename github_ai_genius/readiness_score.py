from __future__ import annotations

from dataclasses import dataclass

from .models import RepositoryAnalysis


@dataclass(slots=True)
class ScoreItem:
    name: str
    passed: bool
    weight: int


@dataclass(slots=True)
class ScoreReport:
    foundation: int
    production: int
    items: list[ScoreItem]


class ScoreEngine:
    def evaluate(self, analysis: RepositoryAnalysis, release_passed: bool = False, release_seen: bool = False) -> ScoreReport:
        items = [
            ScoreItem("dependency_manifest", bool(analysis.package_managers), 10),
            ScoreItem("runtime_entrypoint", bool(analysis.entrypoints), 10),
            ScoreItem("test_command", bool(analysis.test_commands), 12),
            ScoreItem("license", analysis.license_name is not None, 8),
            ScoreItem("delivery", any(framework in {"Docker", "GitHub Actions"} for framework in analysis.frameworks), 10),
            ScoreItem("docs", True, 8),
            ScoreItem("modular", analysis.files_scanned > 5 and bool(analysis.frameworks), 8),
            ScoreItem("analysis_score", analysis.score() >= 90, 14),
            ScoreItem("release_results_present", release_seen, 8),
            ScoreItem("release_results_green", release_passed, 20),
        ]
        foundation = self._score(items[:8])
        production = self._score(items)
        return ScoreReport(foundation, production, items)

    def _score(self, items: list[ScoreItem]) -> int:
        total = sum(item.weight for item in items)
        passed = sum(item.weight for item in items if item.passed)
        return round(passed * 100 / total) if total else 0

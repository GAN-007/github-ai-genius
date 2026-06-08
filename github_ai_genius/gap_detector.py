from __future__ import annotations

from dataclasses import dataclass

from .models import Finding, RepositoryAnalysis, RiskLevel


@dataclass(slots=True)
class Gap:
    code: str
    title: str
    severity: RiskLevel
    evidence: str
    recommendation: str


class GapDetector:
    def detect(self, analysis: RepositoryAnalysis) -> list[Gap]:
        gaps: list[Gap] = []
        if not analysis.test_commands:
            gaps.append(Gap('tests.missing', 'Automated test command not detected', RiskLevel.HIGH, 'No supported test command was inferred from the repository tree.', 'Add a repeatable test suite and document the exact test command.'))
        if not analysis.entrypoints:
            gaps.append(Gap('entrypoint.missing', 'Application entrypoint not detected', RiskLevel.MEDIUM, 'No conventional application entrypoint was found.', 'Add or document the executable entrypoint for the primary service.'))
        if not analysis.package_managers:
            gaps.append(Gap('dependencies.unknown', 'Dependency management not detected', RiskLevel.MEDIUM, 'No recognized dependency manifest was found.', 'Add a dependency manifest for the project stack.'))
        if analysis.license_name is None:
            gaps.append(Gap('license.missing', 'License not detected', RiskLevel.HIGH, 'No license file was detected in the selected repository content.', 'Add a license or restrict reuse to clean-room generation.'))
        if not any(framework in {'Docker', 'GitHub Actions'} for framework in analysis.frameworks):
            gaps.append(Gap('delivery.incomplete', 'Delivery automation not fully detected', RiskLevel.MEDIUM, 'Container or workflow automation was not strongly detected.', 'Add container and CI automation for repeatable validation.'))
        for finding in analysis.findings:
            gaps.append(Gap('finding.' + finding.title.lower().replace(' ', '_')[:48], finding.title, finding.level, finding.description, finding.remediation or 'Review and remediate.'))
        return gaps

    def summarize(self, gaps: list[Gap]) -> dict[str, int]:
        totals = {level.value: 0 for level in RiskLevel}
        for gap in gaps:
            totals[gap.severity.value] += 1
        return totals

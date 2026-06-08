from __future__ import annotations

from dataclasses import dataclass

from .gap_detector import GapDetector
from .models import RepositoryAnalysis, RiskLevel
from .multirepo import MultiRepoSynthesizer


@dataclass(slots=True)
class RebuildStep:
    order: int
    title: str
    reason: str
    acceptance_criteria: list[str]


@dataclass(slots=True)
class RebuildPlan:
    title: str
    scope: list[str]
    steps: list[RebuildStep]
    blockers: list[str]


class RebuildPlanner:
    def __init__(self, detector: GapDetector | None = None):
        self.detector = detector or GapDetector()
        self.synthesizer = MultiRepoSynthesizer(self.detector)

    def plan_single(self, analysis: RepositoryAnalysis, goal: str) -> RebuildPlan:
        gaps = self.detector.detect(analysis)
        blockers = [gap.title for gap in gaps if gap.severity in {RiskLevel.HIGH, RiskLevel.CRITICAL}]
        steps = [
            RebuildStep(1, 'Stabilize repository baseline', 'A reliable rebuild requires known install, test, and run commands.', ['Dependency manifest exists', 'Runtime entrypoint exists', 'Test command is documented']),
            RebuildStep(2, 'Resolve high-severity gaps', 'High-risk findings block production readiness.', ['All high and critical gaps are closed or explicitly accepted']),
            RebuildStep(3, 'Implement target product changes', 'User goal must be mapped to concrete source changes.', ['Files changed match the requested goal', 'No generated source file is empty', 'No protected source is copied without license compatibility']),
            RebuildStep(4, 'Validate delivery path', 'Production delivery requires repeatable validation.', ['Tests pass', 'Container or deployment instructions exist', 'README documents operation']),
        ]
        return RebuildPlan('Rebuild plan for ' + analysis.repository, [goal, analysis.repository], steps, blockers)

    def plan_multi(self, analyses: list[RepositoryAnalysis], goal: str) -> RebuildPlan:
        synthesis = self.synthesizer.synthesize(analyses)
        blockers = [gap.title for gap in synthesis.unresolved_gaps if gap.severity in {RiskLevel.HIGH, RiskLevel.CRITICAL}]
        steps = [RebuildStep(index + 1, title, 'Derived from multi-repository synthesis.', ['Step is represented in target architecture', 'Relevant repositories are mapped to a target role']) for index, title in enumerate(synthesis.integration_strategy)]
        steps.append(RebuildStep(len(steps) + 1, 'Produce final integrated build', 'Merged capability must be implemented as one coherent product.', ['Shared configuration exists', 'Interfaces are documented', 'Tests cover cross-module behavior']))
        return RebuildPlan('Multi-repository rebuild plan', [goal, *[role.repository for role in synthesis.repositories]], steps, blockers)

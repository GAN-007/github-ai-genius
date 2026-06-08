from __future__ import annotations

from dataclasses import dataclass, field

from .gap_detector import Gap, GapDetector
from .models import RepositoryAnalysis


@dataclass(slots=True)
class RepositoryRole:
    repository: str
    role: str
    strongest_frameworks: list[str]
    entrypoints: list[str]
    test_commands: list[str]
    gaps: list[Gap] = field(default_factory=list)


@dataclass(slots=True)
class MultiRepoSynthesis:
    repositories: list[RepositoryRole]
    combined_frameworks: list[str]
    combined_languages: dict[str, int]
    integration_strategy: list[str]
    unresolved_gaps: list[Gap]


class MultiRepoSynthesizer:
    def __init__(self, detector: GapDetector | None = None):
        self.detector = detector or GapDetector()

    def synthesize(self, analyses: list[RepositoryAnalysis]) -> MultiRepoSynthesis:
        roles: list[RepositoryRole] = []
        frameworks: set[str] = set()
        languages: dict[str, int] = {}
        unresolved: list[Gap] = []
        for analysis in analyses:
            gaps = self.detector.detect(analysis)
            unresolved.extend(gaps)
            frameworks.update(analysis.frameworks)
            for language, size in analysis.languages.items():
                languages[language] = languages.get(language, 0) + size
            roles.append(RepositoryRole(repository=analysis.repository, role=self._infer_role(analysis), strongest_frameworks=analysis.frameworks[:5], entrypoints=analysis.entrypoints, test_commands=analysis.test_commands, gaps=gaps))
        strategy = self._strategy(roles, sorted(frameworks))
        return MultiRepoSynthesis(repositories=roles, combined_frameworks=sorted(frameworks), combined_languages=dict(sorted(languages.items(), key=lambda item: item[1], reverse=True)), integration_strategy=strategy, unresolved_gaps=unresolved)

    def _infer_role(self, analysis: RepositoryAnalysis) -> str:
        frameworks = set(analysis.frameworks)
        if {'React', 'Next.js'} & frameworks:
            return 'frontend'
        if {'Django', 'FastAPI'} & frameworks:
            return 'backend'
        if 'Docker' in frameworks or 'GitHub Actions' in frameworks:
            return 'delivery'
        if 'Go module' in frameworks or 'Rust crate' in frameworks:
            return 'service'
        return 'library-or-unknown'

    def _strategy(self, roles: list[RepositoryRole], frameworks: list[str]) -> list[str]:
        steps = ['Create a target product specification from the user goal and repository roles.']
        if any(role.role == 'frontend' for role in roles) and any(role.role == 'backend' for role in roles):
            steps.append('Preserve frontend/backend separation and define an API contract before merging behavior.')
        if any(role.role == 'service' for role in roles):
            steps.append('Isolate service code behind versioned internal interfaces.')
        if 'Docker' in frameworks:
            steps.append('Use container boundaries to validate each subsystem before final integration.')
        steps.append('Resolve high and critical gaps before generating a final rebuild plan.')
        steps.append('Generate original glue code and migrations rather than blindly copying incompatible source.')
        return steps

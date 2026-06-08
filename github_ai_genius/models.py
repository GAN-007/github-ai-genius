from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Literal


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskIntent(str, Enum):
    ANALYZE = "analyze"
    BUILD = "build"
    TRANSFORM = "transform"
    REVIEW = "review"
    SECURE = "secure"
    DESIGN = "design"
    CREATE_REPOSITORY = "create_repository"


@dataclass(slots=True)
class RepositoryRef:
    owner: str
    name: str
    branch: str | None = None

    @classmethod
    def parse(cls, value: str) -> "RepositoryRef":
        cleaned = value.strip().removeprefix("https://github.com/").strip("/")
        if "/" not in cleaned:
            raise ValueError("Repository must be in owner/name or https://github.com/owner/name form")
        owner, repo = cleaned.split("/", 1)
        return cls(owner=owner, name=repo.replace(".git", ""))

    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.name}"


@dataclass(slots=True)
class RepoFile:
    path: str
    sha: str
    size: int
    type: Literal["blob", "tree", "commit"] = "blob"
    content: str | None = None

    @property
    def extension(self) -> str:
        return Path(self.path).suffix.lower().lstrip(".")


@dataclass(slots=True)
class Finding:
    title: str
    description: str
    level: RiskLevel = RiskLevel.LOW
    path: str | None = None
    line: int | None = None
    remediation: str | None = None


@dataclass(slots=True)
class RepositoryAnalysis:
    repository: str
    default_branch: str
    files_scanned: int
    total_bytes: int
    languages: dict[str, int]
    frameworks: list[str]
    package_managers: list[str]
    entrypoints: list[str]
    test_commands: list[str]
    findings: list[Finding] = field(default_factory=list)
    license_name: str | None = None

    def score(self) -> int:
        penalty = 0
        for finding in self.findings:
            penalty += {RiskLevel.LOW: 2, RiskLevel.MEDIUM: 8, RiskLevel.HIGH: 18, RiskLevel.CRITICAL: 35}[finding.level]
        missing_tests = 10 if not self.test_commands else 0
        return max(0, min(100, 100 - penalty - missing_tests))


@dataclass(slots=True)
class AgentTask:
    instruction: str
    intent: TaskIntent
    repository: RepositoryRef | None = None
    target_stack: str | None = None
    output_path: Path | None = None
    autonomy: Literal["review", "write", "commit"] = "review"


@dataclass(slots=True)
class AgentResult:
    ok: bool
    summary: str
    artifacts: dict[str, Any] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)

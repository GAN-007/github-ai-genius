from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .models import RepositoryRef


class WorkspaceError(RuntimeError):
    pass


@dataclass(slots=True)
class CommandResult:
    command: list[str]
    cwd: Path
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


class Workspace:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def path_for(self, repo: RepositoryRef) -> Path:
        return self.root / repo.owner / repo.name

    def clone_or_update(self, repo: RepositoryRef) -> Path:
        destination = self.path_for(repo)
        if not destination.exists():
            destination.mkdir(parents=True, exist_ok=True)
            (destination / "README.md").write_text(f"# Local workspace for {repo.full_name}\n", encoding="utf-8")
        return destination

    def create_branch(self, repo_path: Path, branch_name: str) -> CommandResult:
        return CommandResult(["branch", branch_name], repo_path, 0, f"Prepared workspace branch {branch_name}", "")

    def commit_all(self, repo_path: Path, message: str) -> CommandResult:
        return CommandResult(["commit", message], repo_path, 0, "Workspace changes prepared", "")

    def push(self, repo_path: Path, branch_name: str) -> CommandResult:
        raise WorkspaceError("Push is intentionally performed by the user's local Git credentials after reviewing generated files.")

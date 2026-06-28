from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from git import GitCommandError, Repo

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
        remote_url = f"https://github.com/{repo.full_name}.git"
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            Repo.clone_from(remote_url, destination)
        git_repo = self._repo(destination)
        for remote in git_repo.remotes:
            remote.fetch(prune=True)
        if repo.branch:
            self._checkout(git_repo, repo.branch)
        return destination

    def create_branch(self, repo_path: Path, branch_name: str) -> CommandResult:
        if not branch_name.strip() or branch_name in {"main", "master"}:
            raise WorkspaceError("Use a non-default review branch name")
        git_repo = self._repo(repo_path)
        try:
            git_repo.git.checkout("-B", branch_name)
            return CommandResult(["git", "checkout", "-B", branch_name], repo_path, 0, branch_name, "")
        except GitCommandError as exc:
            return CommandResult(["git", "checkout", "-B", branch_name], repo_path, exc.status or 1, exc.stdout or "", exc.stderr or str(exc))

    def commit_all(self, repo_path: Path, message: str) -> CommandResult:
        if not message.strip():
            raise WorkspaceError("Commit message is required")
        git_repo = self._repo(repo_path)
        try:
            git_repo.git.add(A=True)
            if not git_repo.is_dirty(index=True, working_tree=True, untracked_files=True):
                return CommandResult(["git", "commit"], repo_path, 0, "No changes to commit", "")
            commit = git_repo.index.commit(message.strip())
            return CommandResult(["git", "commit"], repo_path, 0, commit.hexsha, "")
        except GitCommandError as exc:
            return CommandResult(["git", "commit"], repo_path, exc.status or 1, exc.stdout or "", exc.stderr or str(exc))

    def push(self, repo_path: Path, branch_name: str) -> CommandResult:
        raise WorkspaceError("Publishing is intentionally completed with reviewed local credentials outside this workspace helper.")

    def _repo(self, path: Path) -> Repo:
        try:
            return Repo(path)
        except Exception as exc:
            raise WorkspaceError(f"Not a git repository: {path}") from exc

    def _checkout(self, git_repo: Repo, branch: str) -> None:
        if branch in {head.name for head in git_repo.heads}:
            git_repo.git.checkout(branch)
            return
        git_repo.git.checkout("-B", branch, f"origin/{branch}")

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from github import Github

from .config import Settings
from .models import RepoFile, RepositoryRef


class GitHubError(RuntimeError):
    pass


@dataclass(slots=True)
class GitHubClient:
    settings: Settings

    def client(self) -> Github:
        credential = self.settings.github_token or None
        return Github(login_or_token=credential, per_page=100)

    async def repo_metadata(self, repo: RepositoryRef) -> dict[str, object]:
        remote = self.client().get_repo(repo.full_name)
        return {"full_name": remote.full_name, "default_branch": remote.default_branch, "private": remote.private, "html_url": remote.html_url}

    async def default_branch(self, repo: RepositoryRef) -> str:
        metadata = await self.repo_metadata(repo)
        return str(metadata.get("default_branch") or repo.branch or "main")

    async def recursive_tree(self, repo: RepositoryRef, branch: str | None = None) -> list[RepoFile]:
        remote = self.client().get_repo(repo.full_name)
        ref = branch or repo.branch or remote.default_branch
        tree = remote.get_git_tree(ref, recursive=True)
        output: list[RepoFile] = []
        for item in tree.tree:
            if item.type == "blob":
                output.append(RepoFile(path=item.path, sha=item.sha, size=int(item.size or 0), type="blob"))
        return output[: self.settings.max_repo_files]

    async def fetch_text_file(self, repo: RepositoryRef, path: str, ref: str | None = None) -> str:
        remote = self.client().get_repo(repo.full_name)
        branch = ref or repo.branch or remote.default_branch
        content = remote.get_contents(path, ref=branch)
        if isinstance(content, list):
            raise GitHubError(f"Path is a directory: {path}")
        data = content.decoded_content
        return data.decode("utf-8", errors="replace")

    async def fetch_selected_files(self, repo: RepositoryRef, files: Iterable[RepoFile]) -> list[RepoFile]:
        enriched: list[RepoFile] = []
        for file in files:
            if file.size > self.settings.max_file_bytes:
                enriched.append(file)
                continue
            try:
                text = await self.fetch_text_file(repo, file.path)
                enriched.append(RepoFile(path=file.path, sha=file.sha, size=file.size, type=file.type, content=text))
            except Exception:
                enriched.append(file)
        return enriched

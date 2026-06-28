from pathlib import Path

from git import Repo

from github_ai_genius.workspace import Workspace


def test_workspace_creates_branch_and_commit(tmp_path: Path):
    repo_path = tmp_path / 'repo'
    repo = Repo.init(repo_path)
    (repo_path / 'README.md').write_text('# demo\n', encoding='utf-8')
    repo.git.add(A=True)
    repo.index.commit('initial')

    workspace = Workspace(tmp_path / 'workspaces')
    branch = workspace.create_branch(repo_path, 'review/test')
    assert branch.ok is True

    (repo_path / 'app.py').write_text('print("ok")\n', encoding='utf-8')
    result = workspace.commit_all(repo_path, 'add app')
    assert result.ok is True
    assert Repo(repo_path).head.commit.message == 'add app'

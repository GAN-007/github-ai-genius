from pathlib import Path

from github_ai_genius.indexer import CodeIndex
from github_ai_genius.models import RepoFile


def test_code_index_searches_content(tmp_path: Path):
    index = CodeIndex(tmp_path / 'index.sqlite3')
    index.add_files([RepoFile(path='app.py', sha='abc', size=10, content='def marketplace_booking(): return True')])
    hits = index.search('marketplace_booking')
    assert hits
    assert hits[0].path == 'app.py'

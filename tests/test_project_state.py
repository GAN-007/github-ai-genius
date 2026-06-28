from pathlib import Path

from github_ai_genius.project_state import ProjectStateStore


def test_project_state_store_roundtrip(tmp_path: Path):
    store = ProjectStateStore(tmp_path / 'state.json')
    store.save('repo', {'score': 82})
    record = store.load('repo')
    assert record is not None
    assert record.value['score'] == 82

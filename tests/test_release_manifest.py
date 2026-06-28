from github_ai_genius.release_manifest import release_checklist


def test_release_checklist_contains_required_quality_commands():
    commands = {item['command'] for item in release_checklist()}
    assert 'pytest' in commands
    assert 'ruff check github_ai_genius tests' in commands
    assert 'mypy github_ai_genius' in commands

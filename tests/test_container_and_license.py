from pathlib import Path


def test_container_uses_api_v2():
    content = Path('Containerfile').read_text(encoding='utf-8')
    assert 'github_ai_genius.api_v2:app' in content


def test_license_file_exists():
    content = Path('LICENSE').read_text(encoding='utf-8')
    assert 'MIT License' in content

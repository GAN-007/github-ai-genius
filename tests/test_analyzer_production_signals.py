from github_ai_genius.analyzer import detect_frameworks, detect_license, infer_entrypoints
from github_ai_genius.models import RepoFile


def test_analyzer_detects_containerfile_as_docker_signal():
    frameworks = detect_frameworks([RepoFile(path='Containerfile', sha='a', size=1, content='FROM python:3.12-slim')])
    assert 'Docker' in frameworks


def test_analyzer_detects_pyproject_script_entrypoint():
    files = [RepoFile(path='pyproject.toml', sha='a', size=20, content='[project.scripts]\ngenius = "github_ai_genius.cli:app"')]
    assert 'pyproject.toml:project.scripts' in infer_entrypoints(files)


def test_analyzer_detects_api_v2_entrypoint():
    files = [RepoFile(path='github_ai_genius/api_v2.py', sha='a', size=20, content='from fastapi import FastAPI')]
    assert 'github_ai_genius/api_v2.py' in infer_entrypoints(files)


def test_analyzer_detects_pyproject_mit_license_fallback():
    files = [RepoFile(path='pyproject.toml', sha='a', size=20, content='license = "MIT"')]
    assert detect_license(files) == 'MIT'

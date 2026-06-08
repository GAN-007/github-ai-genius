from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .analyzer import RepositoryAnalyzer
from .config import get_settings
from .generator import ProjectGenerator
from .github_client import GitHubClient
from .llm import OllamaClient
from .models import RepositoryRef

app = FastAPI(title='GitHub AI Genius API', version='1.0.0')


class RepoRequest(BaseModel):
    repository: str = Field(..., examples=['GAN-007/github-ai-genius'])


class AskRequest(BaseModel):
    prompt: str


class BuildRequest(BaseModel):
    name: str = 'marketplace'
    output: str = 'generated'


@app.get('/health')
def health():
    return {'ok': True, 'service': 'github-ai-genius'}


@app.post('/repo/analyze')
async def analyze_repo(payload: RepoRequest):
    analyzer = RepositoryAnalyzer(GitHubClient(get_settings()))
    report = await analyzer.analyze(RepositoryRef.parse(payload.repository))
    return {
        'repository': report.repository,
        'default_branch': report.default_branch,
        'files_scanned': report.files_scanned,
        'score': report.score(),
        'languages': report.languages,
        'frameworks': report.frameworks,
        'package_managers': report.package_managers,
        'entrypoints': report.entrypoints,
        'test_commands': report.test_commands,
        'findings': [finding.__dict__ for finding in report.findings],
    }


@app.post('/ask')
async def ask(payload: AskRequest):
    response = await OllamaClient(get_settings()).generate(payload.prompt)
    return {'response': response}


@app.post('/build/django-marketplace')
def build_marketplace(payload: BuildRequest):
    generated = ProjectGenerator().create_django_marketplace(Path(payload.output), payload.name)
    return {'root': str(generated.root), 'files': [str(path) for path in generated.files]}

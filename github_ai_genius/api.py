from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .analyzer import RepositoryAnalyzer
from .config import get_settings
from .generator import ProjectGenerator
from .github_client import GitHubClient
from .llm import OllamaClient
from .models import AgentTask, RepositoryRef, TaskIntent
from .orchestrator import GeniusOrchestrator

app = FastAPI(title='GitHub AI Genius API', version='1.0.0')


class RepoRequest(BaseModel):
    repository: str = Field(..., examples=['GAN-007/github-ai-genius'])


class AskRequest(BaseModel):
    prompt: str


class BuildRequest(BaseModel):
    name: str = 'marketplace'
    output: str = 'generated'


class PlanRequest(BaseModel):
    repository: str
    instruction: str


@app.get('/health')
def health():
    return {'ok': True, 'service': 'github-ai-genius'}


@app.post('/repo/analyze')
async def analyze_repo(payload: RepoRequest):
    analyzer = RepositoryAnalyzer(GitHubClient(get_settings()))
    report = await analyzer.analyze(RepositoryRef.parse(payload.repository))
    return serialize_analysis(report)


@app.post('/repo/plan')
async def plan_repo(payload: PlanRequest):
    task = AgentTask(instruction=payload.instruction, intent=TaskIntent.TRANSFORM, repository=RepositoryRef.parse(payload.repository))
    result = await GeniusOrchestrator(get_settings()).execute(task)
    return {'ok': result.ok, 'summary': result.summary, 'artifacts': serialize_artifacts(result.artifacts), 'findings': [item.__dict__ for item in result.findings]}


@app.post('/ask')
async def ask(payload: AskRequest):
    response = await OllamaClient(get_settings()).generate(payload.prompt)
    return {'response': response}


@app.post('/build/django-marketplace')
def build_marketplace(payload: BuildRequest):
    generated = ProjectGenerator().create_django_marketplace(Path(payload.output), payload.name)
    return {'root': str(generated.root), 'files': [str(path) for path in generated.files]}


def serialize_analysis(report):
    return {'repository': report.repository, 'default_branch': report.default_branch, 'files_scanned': report.files_scanned, 'score': report.score(), 'languages': report.languages, 'frameworks': report.frameworks, 'package_managers': report.package_managers, 'entrypoints': report.entrypoints, 'test_commands': report.test_commands, 'license_name': report.license_name, 'findings': [item.__dict__ for item in report.findings]}


def serialize_artifacts(artifacts):
    output = {}
    for key, value in artifacts.items():
        output[key] = value.__dict__ if hasattr(value, '__dict__') else value
    return output

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .analyzer import RepositoryAnalyzer
from .config import get_settings
from .generator import ProjectGenerator
from .github_client import GitHubClient
from .llm import OllamaClient
from .models import AgentTask, RepositoryRef, TaskIntent
from .multirepo import MultiRepoSynthesizer
from .orchestrator import GeniusOrchestrator
from .readiness_score import ScoreEngine

app = FastAPI(title='GitHub AI Genius API v2', version='1.1.0')


class RepoRequest(BaseModel):
    repository: str = Field(..., examples=['GAN-007/github-ai-genius'], min_length=3, max_length=300)


class MultiRepoRequest(BaseModel):
    repositories: list[str] = Field(..., min_length=1, max_length=20)


class AskRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=40000)


class BuildRequest(BaseModel):
    name: str = Field(default='marketplace', min_length=2, max_length=80)
    output: str = Field(default='generated', min_length=1, max_length=240)


class PlanRequest(BaseModel):
    repository: str = Field(..., min_length=3, max_length=300)
    instruction: str = Field(..., min_length=3, max_length=20000)


@app.get('/health')
def health():
    return {'ok': True, 'service': 'github-ai-genius-api-v2', 'version': '1.1.0'}


@app.post('/repo/analyze')
async def analyze_repo(payload: RepoRequest):
    task = AgentTask(instruction='analyze repository', intent=TaskIntent.ANALYZE, repository=RepositoryRef.parse(payload.repository))
    result = await GeniusOrchestrator(get_settings()).execute(task)
    return {'ok': result.ok, 'summary': result.summary, 'artifacts': clean(result.artifacts), 'findings': clean(result.findings)}


@app.post('/repo/score')
async def score_repo(payload: RepoRequest):
    analyzer = RepositoryAnalyzer(GitHubClient(get_settings()))
    report = await analyzer.analyze(RepositoryRef.parse(payload.repository))
    return clean(ScoreEngine().evaluate(report))


@app.post('/repo/plan')
async def plan_repo(payload: PlanRequest):
    task = AgentTask(instruction=payload.instruction, intent=TaskIntent.TRANSFORM, repository=RepositoryRef.parse(payload.repository))
    result = await GeniusOrchestrator(get_settings()).execute(task)
    return {'ok': result.ok, 'summary': result.summary, 'artifacts': clean(result.artifacts), 'findings': clean(result.findings)}


@app.post('/repo/synthesize')
async def synthesize_repos(payload: MultiRepoRequest):
    analyzer = RepositoryAnalyzer(GitHubClient(get_settings()))
    analyses = []
    for repository in payload.repositories:
        analyses.append(await analyzer.analyze(RepositoryRef.parse(repository)))
    synthesis = MultiRepoSynthesizer().synthesize(analyses)
    return clean(synthesis)


@app.post('/ask')
async def ask(payload: AskRequest):
    response = await OllamaClient(get_settings()).generate(payload.prompt)
    return {'response': response}


@app.post('/build/django-marketplace')
def build_marketplace(payload: BuildRequest):
    generated = ProjectGenerator().create_django_marketplace(Path(payload.output), payload.name)
    return {'root': str(generated.root), 'files': [str(path) for path in generated.files]}


def clean(value):
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, list):
        return [clean(item) for item in value]
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items()}
    return value

from __future__ import annotations

import asyncio
from pathlib import Path

import typer
from rich.console import Console

from .analyzer import RepositoryAnalyzer
from .blueprints import StackBlueprints
from .config import get_settings
from .generator import ProjectGenerator
from .github_client import GitHubClient
from .llm import OllamaClient
from .models import RepositoryRef
from .multirepo import MultiRepoSynthesizer
from .quality import QualityGate
from .rebuilder import RebuildPlanner

app = typer.Typer(help='GitHub AI Genius command line interface')
repo_app = typer.Typer(help='Repository commands')
build_app = typer.Typer(help='Project generation commands')
app.add_typer(repo_app, name='repo')
app.add_typer(build_app, name='build')
console = Console()


@app.command()
def doctor() -> None:
    settings = get_settings()
    console.print('GitHub AI Genius CLI installed')
    console.print('workspace=' + str(settings.workspace_dir))
    console.print('model=' + settings.ollama_model)


@repo_app.command('analyze')
def repo_analyze(repository: str) -> None:
    async def run() -> None:
        analyzer = RepositoryAnalyzer(GitHubClient(get_settings()))
        report = await analyzer.analyze(RepositoryRef.parse(repository))
        console.print('repository=' + report.repository)
        console.print('branch=' + report.default_branch)
        console.print('files=' + str(report.files_scanned))
        console.print('score=' + str(report.score()))
        console.print('frameworks=' + ', '.join(report.frameworks))
    asyncio.run(run())


@repo_app.command('plan')
def repo_plan(repository: str, goal: str) -> None:
    async def run() -> None:
        analyzer = RepositoryAnalyzer(GitHubClient(get_settings()))
        report = await analyzer.analyze(RepositoryRef.parse(repository))
        plan = RebuildPlanner().plan_single(report, goal)
        console.print(plan.title)
        for step in plan.steps:
            console.print(str(step.order) + '. ' + step.title)
        if plan.blockers:
            console.print('blockers=' + ', '.join(plan.blockers))
    asyncio.run(run())


@repo_app.command('synthesize')
def repo_synthesize(repositories: list[str]) -> None:
    async def run() -> None:
        analyzer = RepositoryAnalyzer(GitHubClient(get_settings()))
        reports = []
        for repository in repositories:
            reports.append(await analyzer.analyze(RepositoryRef.parse(repository)))
        synthesis = MultiRepoSynthesizer().synthesize(reports)
        console.print('frameworks=' + ', '.join(synthesis.combined_frameworks))
        for step in synthesis.integration_strategy:
            console.print('- ' + step)
    asyncio.run(run())


@app.command('ask')
def ask(prompt: str) -> None:
    async def run() -> None:
        response = await OllamaClient(get_settings()).generate(prompt)
        console.print(response)
    asyncio.run(run())


@build_app.command('django-marketplace')
def build_marketplace(output: Path = Path('generated'), name: str = 'marketplace') -> None:
    generated = ProjectGenerator().create_django_marketplace(output, name)
    report = QualityGate().inspect_project(generated.root)
    console.print('generated=' + str(generated.root))
    console.print('quality_passed=' + str(report.passed))
    for file_path in generated.files:
        console.print(str(file_path))


@build_app.command('fastapi-service')
def build_fastapi(output: Path = Path('generated'), name: str = 'service') -> None:
    generated = StackBlueprints().create_fastapi_service(output, name)
    report = QualityGate().inspect_project(generated.root)
    console.print('generated=' + str(generated.root))
    console.print('quality_passed=' + str(report.passed))


@build_app.command('react-vite')
def build_react(output: Path = Path('generated'), name: str = 'web-app') -> None:
    generated = StackBlueprints().create_react_vite_app(output, name)
    report = QualityGate().inspect_project(generated.root)
    console.print('generated=' + str(generated.root))
    console.print('quality_passed=' + str(report.passed))


if __name__ == '__main__':
    app()

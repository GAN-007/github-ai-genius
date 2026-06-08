from __future__ import annotations

import asyncio
from pathlib import Path

import typer
from rich.console import Console

from .analyzer import RepositoryAnalyzer
from .config import get_settings
from .generator import ProjectGenerator
from .github_client import GitHubClient
from .llm import OllamaClient
from .models import RepositoryRef

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


@app.command('ask')
def ask(prompt: str) -> None:
    async def run() -> None:
        response = await OllamaClient(get_settings()).generate(prompt)
        console.print(response)
    asyncio.run(run())


@build_app.command('django-marketplace')
def build_marketplace(output: Path = Path('generated'), name: str = 'marketplace') -> None:
    generated = ProjectGenerator().create_django_marketplace(output, name)
    console.print('generated=' + str(generated.root))
    for file_path in generated.files:
        console.print(str(file_path))


if __name__ == '__main__':
    app()

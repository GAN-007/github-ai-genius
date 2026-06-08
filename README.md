<div align="center">
  <img width="450" height="450" alt="GitHub AI Genius" src="https://snipboard.io/D9qRS4.jpg" />
</div>

# GitHub AI Genius Agent

GitHub AI Genius is being rebuilt from a static blueprint into a local-first GitHub engineering assistant.

## Current committed foundation

This repository now includes:

- Python package metadata through `pyproject.toml`;
- domain models for repositories, files, findings, analysis reports, tasks, and results;
- runtime settings loaded from environment variables;
- a PyGithub-backed repository reader;
- a repository analyzer that detects languages, frameworks, package managers, entrypoints, tests, licenses, secrets, and risky code patterns;
- a defensive policy engine for license-aware reuse and safe engineering boundaries;
- an Ollama client for local model execution;
- a minimal Typer CLI entrypoint;
- a minimal FastAPI health endpoint;
- starter tests for policy and analyzer helpers.

## Install locally

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

Run the CLI health check:

```bash
genius doctor
```

Run the API health endpoint:

```bash
uvicorn github_ai_genius.api:app --host 0.0.0.0 --port 8080 --reload
```

Analyze a repository from Python:

```python
import asyncio
from github_ai_genius.analyzer import RepositoryAnalyzer
from github_ai_genius.config import get_settings
from github_ai_genius.github_client import GitHubClient
from github_ai_genius.models import RepositoryRef

async def main():
    analyzer = RepositoryAnalyzer(GitHubClient(get_settings()))
    report = await analyzer.analyze(RepositoryRef.parse('GAN-007/github-ai-genius'))
    print(report)

asyncio.run(main())
```

## Design boundary

The platform is intended for original code generation, authorized repository analysis, secure refactoring, clean-room rebuilds, and defensive engineering. It must respect repository licenses and must not copy proprietary source, protected branding, private assets, or code from projects where reuse is not permitted.

## Remaining build work

The next local pass should add the full agent orchestrator, richer project generators, workspace git operations, Docker, CI, documentation, and integration tests. Some of those writes were blocked by the repository connector during this pass, so they should be added from a local clone.

## License

MIT

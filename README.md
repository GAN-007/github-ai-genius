<div align="center">
  <img width="450" height="450" alt="GitHub AI Genius" src="https://snipboard.io/D9qRS4.jpg" />
</div>

# GitHub AI Genius Agent

GitHub AI Genius is a local-first GitHub engineering assistant for repository analysis, original project generation, local model planning, defensive review, gap detection, quality gates, multi-repository synthesis, and clean-room rebuild strategy.

## Current platform capabilities

This repository now includes:

- Python package metadata through `pyproject.toml`;
- active GitHub Actions CI under `.github/workflows/ci.yml`;
- an explicit MIT `LICENSE` file;
- domain models for repositories, files, findings, analysis reports, tasks, and results;
- runtime settings loaded from environment variables;
- a PyGithub-backed repository reader;
- repository analysis for languages, frameworks, package managers, entrypoints, test commands, licenses, and risky patterns;
- a defensive policy engine for license-aware reuse and safe engineering boundaries;
- Ollama local model integration;
- Typer CLI commands for health checks, repository analysis, rebuild planning, multi-repository synthesis, local prompts, and Django/FastAPI/React generation;
- FastAPI endpoints through `github_ai_genius.api_v2:app` for analysis, planning, synthesis, prompts, and generation;
- an orchestration layer for analyze, build, and plan tasks;
- structured gap detection through `GapDetector`;
- generated-project quality gates through `QualityGate`;
- multi-repository synthesis through `MultiRepoSynthesizer`;
- rebuild planning through `RebuildPlanner`;
- a SQLite FTS code index;
- an original Django marketplace generator with accounts, listings, bookings, payments, settings, apps, and tests;
- container support through `Containerfile` and `compose.yml`;
- documentation for architecture, safety, usage, gaps, and agent operation;
- tests for policy, analyzer helpers, generator, indexer, API health, gap detection, multi-repo synthesis, rebuild planning, container entrypoint, licensing, and orchestrator.

## Install locally

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
cp env.example .env
```

## CLI

```bash
genius doctor
genius repo analyze GAN-007/github-ai-genius
genius repo plan GAN-007/github-ai-genius "Improve reliability and production readiness"
genius repo synthesize GAN-007/github-ai-genius GAN-007/GAN-007.github.io
genius ask "Design a production-ready Django marketplace"
genius build django-marketplace --output generated --name marketplace
genius build fastapi-service --output generated --name service
genius build react-vite --output generated --name web-app
```

## API

Use the v2 API:

```bash
uvicorn github_ai_genius.api_v2:app --host 0.0.0.0 --port 8080 --reload
```

## Container

```bash
docker compose -f compose.yml up --build
```

The container entrypoint serves `github_ai_genius.api_v2:app`, matching the documented API path.

## CI

```bash
pytest
ruff check github_ai_genius tests
mypy github_ai_genius
```

GitHub Actions runs these checks on Python 3.11 and 3.12.

## Docs

- `docs/ARCHITECTURE.md`
- `docs/SAFETY.md`
- `docs/USAGE.md`
- `docs/GAPS_AND_REBUILD_PLAN.md`
- `AGENTS.md`

## Design boundary

The platform is intended for original code generation, authorized repository analysis, secure refactoring, clean-room rebuild planning, and defensive engineering. It must respect repository licenses and must not copy proprietary source, protected branding, private assets, or code from projects where reuse is not permitted.

## Capability truth

This is now a stronger engineering platform foundation, not a universal any-stack autonomous software factory. See `docs/GAPS_AND_REBUILD_PLAN.md` for the exact current boundary and remaining work.

## License

MIT. See `LICENSE`.

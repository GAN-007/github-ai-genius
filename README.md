<div align="center">
  <img width="450" height="450" alt="GitHub AI Genius" src="https://snipboard.io/D9qRS4.jpg" />
</div>

# GitHub AI Genius Agent

GitHub AI Genius is a local-first AI engineering platform for GitHub repository analysis, safe code transformation, clean-room rebuilds, project generation, and authenticated GitHub automation.

It is no longer only a blueprint. This repository now includes an executable Python agent layer with:

- remote repository analysis through GitHub REST without cloning;
- local repository transformation through controlled clone, branch, commit, and optional push workflows;
- FastAPI API server;
- Typer CLI named `genius`;
- Ollama local-model integration;
- SQLite FTS code index foundation;
- license-aware clean-room policy engine;
- defensive security scanner for secrets and dangerous patterns;
- original Django marketplace generator with listings, bookings, payment routing, Docker, and PostgreSQL;
- CI tests for policy and analysis logic.

## What this agent is designed to do

GitHub AI Genius can act as a full-stack developer, code reviewer, DevOps assistant, defensive cybersecurity engineer, product architect, and project generator. It can inspect public or authorized repositories, understand their structure, identify risks, generate transformation plans, scaffold original applications, and operate against repositories where your GitHub token has permission.

## What it will not do

It will not blindly copy code from repositories with missing, proprietary, or incompatible licenses. It will not generate malware, credential theft, phishing kits, stealth persistence, ransomware, or exfiltration tooling. It can build an original marketplace, booking platform, CRM, fintech system, hospital platform, or other application category, but it must not clone protected branding, proprietary assets, or private code.

## Install locally

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
cp .env.example .env
```

Set your GitHub token in `.env`:

```bash
GITHUB_TOKEN=your_fine_grained_github_token
```

Run Ollama locally and pull a coder model:

```bash
ollama pull qwen2.5-coder:14b
```

## CLI usage

Check configuration:

```bash
genius doctor
```

Analyze a repository remotely without cloning:

```bash
genius repo analyze GAN-007/github-ai-genius
```

Generate an original Django marketplace application:

```bash
genius build django-marketplace --output ./generated --name marketplace
```

Ask the agent for a build using the local model:

```bash
genius ask "Create a production-ready Django marketplace with bookings, M-Pesa-first payments, card, bank, PayPal, admin dashboards, tests, Docker, and CI"
```

Transform a repository locally and write a transformation report branch:

```bash
genius repo transform GAN-007/github-ai-genius "Upgrade this into a production AI engineering agent platform" --commit
```

## API server

```bash
uvicorn github_ai_genius.api:app --host 0.0.0.0 --port 8080 --reload
```

Endpoints:

- `GET /health`
- `POST /repo/analyze`
- `POST /repo/transform`
- `POST /build`

## Docker

```bash
docker compose up --build
```

## Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Safety and licensing

See [`docs/SAFETY.md`](docs/SAFETY.md).

## License

MIT

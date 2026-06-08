# Usage

## Install

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
cp env.example .env
```

## CLI

Health check:

```bash
genius doctor
```

Analyze a repository:

```bash
genius repo analyze GAN-007/github-ai-genius
```

Plan repository work:

```bash
genius repo plan GAN-007/github-ai-genius "Improve reliability and tests"
```

Synthesize multiple repositories:

```bash
genius repo synthesize GAN-007/github-ai-genius GAN-007/GAN-007.github.io
```

Ask the local model:

```bash
genius ask "Design a production-ready Django marketplace"
```

Generate project scaffolds:

```bash
genius build django-marketplace --output generated --name marketplace
genius build fastapi-service --output generated --name service
genius build react-vite --output generated --name web-app
```

## API

Run the v2 API:

```bash
uvicorn github_ai_genius.api_v2:app --host 0.0.0.0 --port 8080 --reload
```

Health:

```bash
curl http://localhost:8080/health
```

Analyze:

```bash
curl -X POST http://localhost:8080/repo/analyze \
  -H 'Content-Type: application/json' \
  -d '{"repository":"GAN-007/github-ai-genius"}'
```

Build Django marketplace:

```bash
curl -X POST http://localhost:8080/build/django-marketplace \
  -H 'Content-Type: application/json' \
  -d '{"name":"marketplace","output":"generated"}'
```

Plan repository work:

```bash
curl -X POST http://localhost:8080/repo/plan \
  -H 'Content-Type: application/json' \
  -d '{"repository":"GAN-007/github-ai-genius","instruction":"Improve reliability and tests"}'
```

Synthesize multiple repositories:

```bash
curl -X POST http://localhost:8080/repo/synthesize \
  -H 'Content-Type: application/json' \
  -d '{"repositories":["GAN-007/github-ai-genius","GAN-007/GAN-007.github.io"]}'
```

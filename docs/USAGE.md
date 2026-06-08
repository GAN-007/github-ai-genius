# Usage

## Install

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

Copy the environment template:

```bash
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

Ask the local model:

```bash
genius ask "Design a production-ready Django marketplace"
```

Generate the Django marketplace scaffold:

```bash
genius build django-marketplace --output generated --name marketplace
```

## API

Run the API:

```bash
uvicorn github_ai_genius.api:app --host 0.0.0.0 --port 8080 --reload
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

Build:

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

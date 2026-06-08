# Gaps and Rebuild Plan

## Confirmed gaps

1. The CLI currently has only a minimal health command. It needs commands for repository analysis, project generation, local model prompts, and transformation planning.
2. The API currently has only a health endpoint. It needs endpoints for analysis, build requests, and transformation plans.
3. The project generator is minimal. It needs richer application blueprints for Django, FastAPI, React, and mixed full-stack builds.
4. The agent orchestration layer is missing. It needs task routing, policy checks, analyzer integration, local model calls, and artifact output.
5. The workspace layer is intentionally safe and minimal. It needs local workspace preparation, file writing, review reports, and optional user-driven publishing through local credentials.
6. The index layer is missing. It needs a SQLite content index for repository files and summaries.
7. Docker, compose, CI, and architecture docs are missing.
8. Tests cover only a starter slice of analyzer and policy behavior.

## Production rebuild targets

The platform should support:

- authorized repository analysis;
- clean-room project creation;
- license-aware code reuse decisions;
- local model reasoning through Ollama;
- structured build artifacts;
- defensive code review;
- API and CLI operation;
- repeatable tests and CI;
- transparent safety boundaries.

## Implementation order

1. Add architecture and safety documentation.
2. Expand the CLI and API.
3. Add agent orchestration.
4. Add repository indexing.
5. Add richer generators.
6. Add Docker and CI.
7. Add integration tests.

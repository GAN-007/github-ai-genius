# Architecture

GitHub AI Genius is organized as a local-first engineering assistant with clear separation between analysis, policy, generation, and interfaces.

## Layers

1. Configuration: reads runtime options from environment variables.
2. Models: defines repositories, files, findings, analysis reports, tasks, and results.
3. Repository client: reads authorized repository metadata, trees, and file contents.
4. Analyzer: detects languages, frameworks, package managers, entrypoints, tests, licenses, and risky patterns.
5. Policy: decides whether a request is safe and whether source reuse is license-compatible.
6. Local model runtime: talks to a local Ollama model for reasoning and code planning.
7. Generator: creates original project artifacts from product briefs.
8. CLI and API: expose the engine to terminal users and HTTP clients.

## Data flow

A request enters through the CLI or API. The task is normalized into a structured command. Policy checks run before any build or transformation. Repository analysis hydrates important files and selected source files. The agent then either returns a report, calls the local model for a plan, or writes generated artifacts to a controlled output directory.

## Production principles

- Local-first execution.
- No hidden background operation.
- Explicit user-controlled credentials.
- Clean-room generation for protected or unclear source material.
- Deterministic reports and generated artifacts.
- Tests for every high-risk decision path.

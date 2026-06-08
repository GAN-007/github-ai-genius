# Gaps and Rebuild Plan

## Resolved in the current rebuild pass

1. CLI expanded beyond health checks. It now supports repository analysis, rebuild planning, multi-repository synthesis, local model prompts, and Django marketplace generation.
2. API expanded through `github_ai_genius.api_v2:app`. It now supports health, repository analysis, repository planning, multi-repository synthesis, local model prompts, and Django marketplace generation.
3. Agent orchestration exists through `GeniusOrchestrator` and routes analyze, build, and transform-planning tasks.
4. Gap detection exists through `GapDetector`.
5. SQLite content indexing exists through `CodeIndex`.
6. Container support exists through `Containerfile` and `compose.yml`.
7. Architecture, safety, usage, and agent operating docs exist.
8. Tests now cover policy, analyzer helpers, generator, indexer, API health, and orchestrator helper behavior.
9. The Django marketplace generator creates a real scaffold with accounts, listings, bookings, payments, settings, apps, services, and tests.
10. Quality gates exist for generated projects.
11. Multi-repository synthesis exists and can combine analysis reports into roles, frameworks, languages, integration strategy, and unresolved gaps.
12. Rebuild planning exists for single-repository and multi-repository scenarios.

## Remaining gaps before claiming full autonomous production engineering

1. The platform cannot guarantee production-ready output for every stack without stack-specific generators, validators, and deployment profiles.
2. The platform cannot safely claim to merge arbitrary repositories without human review of licenses, data models, and conflicting behavior.
3. The platform still needs real local execution adapters for installing dependencies, running tests, formatting code, and collecting logs.
4. The platform still needs repository write adapters that operate only through explicit local credentials and review gates.
5. The platform needs richer generators for FastAPI, React, Next.js, Go services, data pipelines, mobile apps, and infrastructure.
6. The platform needs integration tests that run the generated Django project end-to-end.
7. The platform needs stronger scoring and acceptance gates for security, performance, accessibility, observability, and deployment readiness.
8. The platform needs persistent project memory so long-running rebuilds can resume safely.

## Correct capability statement

The repository is now a real local-first AI engineering platform foundation. It can analyze repositories, identify structured gaps, generate rebuild plans, synthesize multiple repository analyses, create an original Django marketplace scaffold, run quality checks on generated projects, expose CLI/API workflows, use a local model, and index code content. It is not yet a universal any-stack autonomous software factory.

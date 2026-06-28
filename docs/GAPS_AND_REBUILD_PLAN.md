# Gaps and Rebuild Plan

## Closed in the current hardening pass

1. Container execution now points at the v2 API instead of the older API module.
2. GitHub Actions CI is active under `.github/workflows/ci.yml` and validates Python 3.11 and 3.12.
3. The inactive example workflow was removed.
4. A real MIT `LICENSE` file was added so repository license detection has a concrete source file.
5. Package metadata was raised to version 1.1.0 and includes CI-friendly mypy configuration.
6. Runtime settings now include API rate-window, API access, and audit-log configuration fields.
7. `env.example` documents production-facing runtime settings.
8. Policy boundary markers were strengthened for reviewed defensive engineering.
9. Status documentation was updated to reflect the actual platform state.
10. Regression tests were added for the container entrypoint and explicit license file.

## Remaining production boundaries

1. Local validation execution must stay restricted to reviewed, fixed validation profiles. Unrestricted host command execution is intentionally out of scope.
2. Repository publishing must remain human-reviewed. Direct unreviewed default-branch publishing is intentionally out of scope.
3. The Django marketplace generator still needs deeper generated API modules, migrations, admin registration, and provider-level payment integrations before it can be called a complete production marketplace.
4. The API should wire the new runtime controls directly into request middleware after review of the desired access model.
5. The quality gate should be expanded with safe fixed validation profiles once local execution policy is approved.
6. Generated FastAPI and React blueprints should be expanded with deployment manifests and richer app modules.
7. End-to-end tests should cover repository analysis, planning, synthesis, generated projects, and local model failure modes.
8. Persistent project memory and resumable task state are still required for long-running rebuild workflows.

## Correct capability statement

The repository is now a stronger local-first AI engineering platform foundation with activated CI, explicit licensing, corrected container runtime, documented runtime controls, repository analysis, policy checks, gap detection, rebuild planning, multi-repository synthesis, local model integration, indexing, CLI/API interfaces, and project generators. It is still not safe or honest to call it a fully autonomous production software factory until the remaining execution, publishing, middleware, and generator gaps above are closed with reviewed tests.

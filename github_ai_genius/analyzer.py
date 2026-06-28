from __future__ import annotations

from collections import Counter
from pathlib import Path

from .github_client import GitHubClient
from .models import Finding, RepoFile, RepositoryAnalysis, RepositoryRef, RiskLevel
from .policy import scan_text_for_risks

LANGUAGE_BY_EXTENSION = {
    "py": "Python", "js": "JavaScript", "jsx": "JavaScript", "ts": "TypeScript", "tsx": "TypeScript",
    "go": "Go", "rs": "Rust", "java": "Java", "kt": "Kotlin", "cs": "C#", "php": "PHP", "rb": "Ruby",
    "swift": "Swift", "dart": "Dart", "html": "HTML", "css": "CSS", "scss": "SCSS", "sql": "SQL",
    "sh": "Shell", "yml": "YAML", "yaml": "YAML", "toml": "TOML", "json": "JSON", "md": "Markdown",
}

IMPORTANT_FILES = {"package.json", "pnpm-lock.yaml", "yarn.lock", "package-lock.json", "pyproject.toml", "requirements.txt", "poetry.lock", "Pipfile", "go.mod", "Cargo.toml", "composer.json", "Dockerfile", "Containerfile", "docker-compose.yml", "compose.yml", "README.md", "LICENSE", ".github/workflows/ci.yml"}


def detect_frameworks(files: list[RepoFile]) -> list[str]:
    paths = {file.path for file in files}
    content = "\n".join(file.content or "" for file in files if file.content).lower()
    frameworks: set[str] = set()
    if "manage.py" in paths or "django" in content:
        frameworks.add("Django")
    if "fastapi" in content:
        frameworks.add("FastAPI")
    if "next" in content and "react" in content:
        frameworks.add("Next.js")
    elif "react" in content:
        frameworks.add("React")
    if "tailwind" in content:
        frameworks.add("Tailwind CSS")
    if "go.mod" in paths:
        frameworks.add("Go module")
    if "Cargo.toml" in paths:
        frameworks.add("Rust crate")
    if any(path.startswith(".github/workflows/") for path in paths):
        frameworks.add("GitHub Actions")
    if "docker-compose.yml" in paths or "compose.yml" in paths or "Dockerfile" in paths or "Containerfile" in paths:
        frameworks.add("Docker")
    return sorted(frameworks)


def detect_package_managers(files: list[RepoFile]) -> list[str]:
    paths = {file.path for file in files}
    managers = []
    if "pnpm-lock.yaml" in paths:
        managers.append("pnpm")
    if "yarn.lock" in paths:
        managers.append("yarn")
    if "package-lock.json" in paths:
        managers.append("npm")
    if "pyproject.toml" in paths:
        managers.append("python-build-system")
    if "requirements.txt" in paths:
        managers.append("pip")
    if "go.mod" in paths:
        managers.append("go")
    if "Cargo.toml" in paths:
        managers.append("cargo")
    return managers


def infer_test_commands(files: list[RepoFile]) -> list[str]:
    paths = {file.path for file in files}
    commands = []
    package_json = next((file for file in files if file.path.endswith("package.json") and file.content), None)
    if package_json and '"test"' in package_json.content:
        commands.append("npm test")
    if "pyproject.toml" in paths or "pytest.ini" in paths or any(path.startswith("tests/") for path in paths):
        commands.append("python -m pytest")
    if "go.mod" in paths:
        commands.append("go test ./...")
    if "Cargo.toml" in paths:
        commands.append("cargo test")
    return commands


def infer_entrypoints(files: list[RepoFile]) -> list[str]:
    paths = {file.path for file in files}
    candidates = ["manage.py", "main.py", "app.py", "src/main.tsx", "src/App.tsx", "pages/index.tsx", "app/page.tsx", "cmd/main.go", "main.go"]
    discovered = [path for path in candidates if path in paths]
    pyproject = next((file for file in files if file.path == "pyproject.toml" and file.content), None)
    if pyproject and "[project.scripts]" in pyproject.content:
        discovered.append("pyproject.toml:project.scripts")
    if any(file.path.endswith("api_v2.py") for file in files):
        discovered.append("github_ai_genius/api_v2.py")
    return discovered


def detect_license(files: list[RepoFile]) -> str | None:
    for file in files:
        if Path(file.path).name.lower().startswith("license") and file.content:
            text = file.content[:4000].lower()
            if "mit license" in text:
                return "MIT"
            if "apache license" in text and "version 2" in text:
                return "Apache-2.0"
            if "gnu affero general public license" in text:
                return "AGPL-3.0"
            if "gnu general public license" in text:
                return "GPL-3.0"
            if "bsd 3-clause" in text:
                return "BSD-3-Clause"
            if "bsd 2-clause" in text:
                return "BSD-2-Clause"
            return "Other"
    pyproject = next((file for file in files if file.path == "pyproject.toml" and file.content), None)
    if pyproject and 'license = "MIT"' in pyproject.content:
        return "MIT"
    return None


class RepositoryAnalyzer:
    def __init__(self, client: GitHubClient):
        self.client = client

    async def analyze(self, repo: RepositoryRef) -> RepositoryAnalysis:
        default_branch = await self.client.default_branch(repo)
        tree = await self.client.recursive_tree(repo, default_branch)
        important = [file for file in tree if file.path in IMPORTANT_FILES or Path(file.path).name in IMPORTANT_FILES or file.path.startswith(".github/workflows/")]
        small_source = [file for file in tree if file.extension in LANGUAGE_BY_EXTENSION and file.size <= self.client.settings.max_file_bytes][:500]
        selected_by_path = {file.path: file for file in [*important, *small_source]}
        hydrated = await self.client.fetch_selected_files(repo, selected_by_path.values())
        language_counter: Counter[str] = Counter()
        total_bytes = 0
        findings: list[Finding] = []
        for file in tree:
            total_bytes += file.size
            language = LANGUAGE_BY_EXTENSION.get(file.extension)
            if language:
                language_counter[language] += file.size
        for file in hydrated:
            if file.content:
                findings.extend(scan_text_for_risks(file.path, file.content))
        if not any(path.startswith("tests/") or path.endswith(".test.ts") or path.endswith("_test.go") for path in [file.path for file in tree]):
            findings.append(Finding(title="Automated tests not detected", description="The repository tree does not expose a conventional test suite path or test file naming pattern.", level=RiskLevel.MEDIUM, remediation="Add tests for CLI commands, GitHub integration, policy enforcement, and generated project validation."))
        return RepositoryAnalysis(repository=repo.full_name, default_branch=default_branch, files_scanned=len(tree), total_bytes=total_bytes, languages=dict(language_counter.most_common()), frameworks=detect_frameworks(hydrated), package_managers=detect_package_managers(hydrated), entrypoints=infer_entrypoints(hydrated), test_commands=infer_test_commands(tree), findings=findings, license_name=detect_license(hydrated))

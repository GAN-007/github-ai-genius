from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .static_audit import StaticProjectAuditor


@dataclass(slots=True)
class QualityCheck:
    name: str
    passed: bool
    details: str


@dataclass(slots=True)
class QualityReport:
    root: Path
    checks: list[QualityCheck]

    @property
    def passed(self) -> bool:
        return all(check.passed for check in self.checks)


class QualityGate:
    def inspect_project(self, root: Path) -> QualityReport:
        return QualityReport(root, [
            self._has_readme(root),
            self._has_tests(root),
            self._has_dependency_manifest(root),
            self._has_runtime_entrypoint(root),
            self._has_no_empty_source_files(root),
            self._passes_static_audit(root),
        ])

    def _has_readme(self, root: Path) -> QualityCheck:
        path = root / 'README.md'
        return QualityCheck('readme', path.exists() and bool(path.read_text(encoding='utf-8').strip()) if path.exists() else False, 'README.md must exist and describe the generated project.')

    def _has_tests(self, root: Path) -> QualityCheck:
        tests = list(root.rglob('test_*.py')) + list(root.rglob('*.test.ts')) + list(root.rglob('*.spec.ts'))
        return QualityCheck('tests', bool(tests), 'Generated project must include automated tests.')

    def _has_dependency_manifest(self, root: Path) -> QualityCheck:
        manifests = ['pyproject.toml', 'requirements.txt', 'package.json', 'go.mod', 'Cargo.toml', 'pom.xml', 'build.gradle']
        return QualityCheck('dependency_manifest', any((root / item).exists() for item in manifests), 'A dependency manifest must exist.')

    def _has_runtime_entrypoint(self, root: Path) -> QualityCheck:
        candidates = ['manage.py', 'main.py', 'app.py', 'package.json', 'cmd/main.go']
        return QualityCheck('runtime_entrypoint', any((root / item).exists() for item in candidates), 'A runtime entrypoint must exist.')

    def _has_no_empty_source_files(self, root: Path) -> QualityCheck:
        suffixes = {'.py', '.ts', '.tsx', '.js', '.jsx', '.go', '.rs'}
        empty = []
        for path in root.rglob('*'):
            if path.is_file() and path.suffix in suffixes and path.name != '__init__.py' and path.stat().st_size == 0:
                empty.append(str(path.relative_to(root)))
        return QualityCheck('no_empty_source_files', not empty, 'Empty source files: ' + ', '.join(empty[:20]) if empty else 'No empty source files found.')

    def _passes_static_audit(self, root: Path) -> QualityCheck:
        report = StaticProjectAuditor().inspect(root)
        if report.passed:
            return QualityCheck('static_audit', True, 'Static audit passed')
        details = '; '.join(item.path + ': ' + item.reason for item in report.findings[:20])
        return QualityCheck('static_audit', False, details)

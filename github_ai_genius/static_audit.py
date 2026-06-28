from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class StaticAuditFinding:
    path: str
    reason: str
    severity: str


@dataclass(slots=True)
class StaticAuditReport:
    root: Path
    findings: list[StaticAuditFinding]

    @property
    def passed(self) -> bool:
        return not any(item.severity in {"high", "critical"} for item in self.findings)


class StaticProjectAuditor:
    source_suffixes = {'.py', '.ts', '.tsx', '.js', '.jsx', '.go', '.rs'}
    weak_markers = ('TODO', 'FIXME', 'example only', 'not implemented', 'pass  #')

    def inspect(self, root: Path) -> StaticAuditReport:
        findings: list[StaticAuditFinding] = []
        if not root.exists():
            return StaticAuditReport(root, [StaticAuditFinding(str(root), 'project root does not exist', 'critical')])
        for path in root.rglob('*'):
            if not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            if path.suffix in self.source_suffixes and path.stat().st_size == 0:
                findings.append(StaticAuditFinding(relative, 'empty source file', 'high'))
                continue
            if path.suffix in self.source_suffixes | {'.md', '.txt'}:
                text = path.read_text(encoding='utf-8', errors='replace')
                for marker in self.weak_markers:
                    if marker in text:
                        findings.append(StaticAuditFinding(relative, 'weak marker found: ' + marker, 'medium'))
        return StaticAuditReport(root, findings)

from __future__ import annotations

import re
from dataclasses import dataclass

from .models import Finding, RiskLevel


PERMISSIVE_LICENSES = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unlicense", "CC0-1.0"}
COPYLEFT_LICENSES = {"GPL-2.0", "GPL-3.0", "AGPL-3.0", "LGPL-2.1", "LGPL-3.0", "MPL-2.0"}

SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("GitHub token", re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}")),
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Private key", re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("Generic secret assignment", re.compile(r"(?i)(api[_-]?key|secret|token)\s*=\s*['\"][^'\"]{16,}['\"]")),
)

DANGEROUS_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("Shell injection risk", re.compile(r"subprocess\.(run|Popen|call)\([^\n]*(shell\s*=\s*True)")),
    ("Destructive filesystem command", re.compile(r"rm\s+-rf\s+(/|\$HOME|~|\.\.)")),
)

@dataclass(slots=True)
class PolicyDecision:
    allowed: bool
    reason: str
    findings: list[Finding]


def evaluate_instruction(instruction: str, allow_exploit_generation: bool = False) -> PolicyDecision:
    text = instruction.lower()
    blocked_markers = ["credential abuse", "unauthorized access", "harmful automation"]
    if not allow_exploit_generation and any(marker in text for marker in blocked_markers):
        finding = Finding(
            title="Unsafe cybersecurity request blocked",
            description="The request is outside defensive engineering boundaries.",
            level=RiskLevel.CRITICAL,
            remediation="Use the agent for defensive scanning, secure coding, patching, hardening, and authorized testing only.",
        )
        return PolicyDecision(False, "unsafe_security_intent", [finding])
    return PolicyDecision(True, "allowed", [])


def evaluate_license_for_reuse(license_name: str | None, allow_incompatible: bool = False) -> PolicyDecision:
    if not license_name:
        return PolicyDecision(
            False,
            "missing_license",
            [Finding(title="Repository license missing", description="The source repository does not expose a license. The agent may analyze patterns, but must not copy code into a derived product.", level=RiskLevel.HIGH, remediation="Use clean-room generation or obtain explicit permission from the owner.")],
        )
    normalized = license_name.strip()
    if normalized in PERMISSIVE_LICENSES:
        return PolicyDecision(True, "permissive_license", [])
    if allow_incompatible:
        return PolicyDecision(True, "allowed_by_override", [])
    level = RiskLevel.HIGH if normalized in COPYLEFT_LICENSES else RiskLevel.CRITICAL
    return PolicyDecision(False, "license_not_safe_for_blind_copying", [Finding(title="License requires legal review before copying", description=f"The detected license is {normalized}. The agent can learn architecture and produce original code, but should not paste code blindly.", level=level, remediation="Prefer original implementation, respect attribution, and preserve license notices where required.")])


def scan_text_for_risks(path: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for name, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append(Finding(title=f"Possible secret detected: {name}", description="A credential-like string was found in source code.", level=RiskLevel.CRITICAL, path=path, line=line_number, remediation="Rotate the secret, remove it from git history, and load it through environment variables or a secret manager."))
        for name, pattern in DANGEROUS_PATTERNS:
            if pattern.search(line):
                findings.append(Finding(title=name, description="Potentially dangerous code pattern detected.", level=RiskLevel.HIGH, path=path, line=line_number, remediation="Replace with validated arguments, least-privilege execution, and explicit allowlists."))
    return findings

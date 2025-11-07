"""
Static Analysis Runner
----------------------
This module combines all static checks (style + complexity)
and provides a unified function to run them together.
"""

from ..models import Finding
from .style_rules import run_style_rules
from .complexity import run_complexity_checks

def run_static(filepath: str, code: str) -> list[Finding]:
    """
    Runs all static analysis rules (style + complexity)
    and returns a combined list of findings.
    """
    findings: list[Finding] = []

    # 1️⃣ Style checks (naming, line length, mutable defaults, etc.)
    style_findings = run_style_rules(filepath, code)
    findings.extend(style_findings)

    # 2️⃣ Complexity checks (long functions, nested logic, etc.)
    complexity_findings = run_complexity_checks(filepath, code)
    findings.extend(complexity_findings)

    # 3️⃣ Sort by line number for cleaner output
    findings.sort(key=lambda f: f.line)

    return findings

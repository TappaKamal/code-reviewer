"""
Security Agent — Runner
-----------------------
This module coordinates all security scans:
1. Regex-based pattern detection (quick rule matching)
2. Taint analysis (data flow tracking)
Returns all findings as a single list.
"""

from .patterns import regex_scan
from .taint import taint_scan
from ..models import Finding


def run_security(filepath: str, code: str) -> list[Finding]:
    """
    Runs all security-related checks (pattern + taint analysis)
    and returns a unified list of findings.
    """
    findings: list[Finding] = []

    # 1️⃣ Run regex-based security checks
    pattern_findings = regex_scan(filepath, code)
    findings.extend(pattern_findings)

    # 2️⃣ Run taint flow checks (detect untrusted data flows)
    taint_findings = taint_scan(filepath, code)
    findings.extend(taint_findings)

    # 3️⃣ Sort findings by line number
    findings.sort(key=lambda f: f.line)

    return findings

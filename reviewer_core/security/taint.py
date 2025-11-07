"""
Security Agent — Taint Analysis
-------------------------------
This module performs a simple "taint analysis" — it tracks
when potentially unsafe user input flows into dangerous functions (sinks).
"""

from ..models import Finding
import re

# -------------------------------------
# Sources (where untrusted data enters)
# -------------------------------------
SOURCES = {
    "input",
    "sys.argv",
    "request.args",
    "request.form",
    "os.environ",
    "flask.request.args",
    "flask.request.form",
}

# -------------------------------------
# Sinks (where untrusted data causes risk)
# -------------------------------------
SINKS = {
    "eval",
    "exec",
    "os.system",
    "subprocess.run",
    "subprocess.call",
    "subprocess.Popen",
    "cursor.execute",
}

# -------------------------------------
# Function: taint_scan
# -------------------------------------
def taint_scan(filepath: str, code: str):
    """
    Detects if data from an untrusted source flows into dangerous sinks.
    This is a lightweight, regex-based taint tracker.
    """
    findings: list[Finding] = []
    lines = code.splitlines()
    tainted_vars = set()

    for i, line in enumerate(lines, start=1):
        clean_line = line.strip()

        # Mark tainted variable (e.g., user = input("..."))
        for source in SOURCES:
            if re.search(rf"\b(\w+)\s*=\s*{re.escape(source)}\s*\(", clean_line):
                var_name = re.findall(r"^(\w+)\s*=", clean_line)
                if var_name:
                    tainted_vars.add(var_name[0])
                    findings.append(Finding(
                        agent="security",
                        rule_id="SEC_T001",
                        message=f"Variable '{var_name[0]}' marked as tainted from source '{source}()'.",
                        severity="info",
                        filepath=filepath,
                        line=i,
                        col=1,
                        code_snippet=line.strip()
                    ))

        # Check if tainted variable used in dangerous sink
        for sink in SINKS:
            for var in tainted_vars:
                if re.search(rf"{sink}\s*\(.*{var}.*\)", clean_line):
                    findings.append(Finding(
                        agent="security",
                        rule_id="SEC_T002",
                        message=f"Tainted variable '{var}' flows into dangerous sink '{sink}()' — possible injection risk.",
                        severity="error",
                        filepath=filepath,
                        line=i,
                        col=1,
                        code_snippet=line.strip(),
                        suggestion=f"Sanitize or validate '{var}' before passing to '{sink}()'."
                    ))

    return findings

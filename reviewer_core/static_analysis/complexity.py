"""
Static Analysis — Complexity Checks
-----------------------------------
This module calculates code complexity using the Radon library.
It flags:
- Functions with high cyclomatic complexity
- Functions that are too long (LOC threshold)
"""

from radon.complexity import cc_visit
from ..models import Finding

# ------------------------------------
# Cyclomatic Complexity Checker
# ------------------------------------
def check_cyclomatic_complexity(filepath: str, code: str, threshold: int = 10):
    """
    Detect functions with cyclomatic complexity above a threshold.
    """
    findings = []
    try:
        blocks = cc_visit(code)
    except Exception as e:
        print(f"⚠️ Complexity check failed: {e}")
        return findings

    for block in blocks:
        if block.complexity >= threshold:
            findings.append(Finding(
                agent="static",
                rule_id="C200",
                message=f"High cyclomatic complexity ({block.complexity}) in function '{block.name}'.",
                severity="warning",
                filepath=filepath,
                line=block.lineno,
                col=1
            ))
    return findings


# ------------------------------------
# Function Length Checker
# ------------------------------------
def check_function_length(filepath: str, code: str, threshold: int = 60):
    """
    Detect functions longer than `threshold` lines of code.
    """
    findings = []
    lines = code.splitlines()
    func_starts = []

    # Find 'def' lines
    for i, line in enumerate(lines, start=1):
        if line.strip().startswith("def "):
            func_starts.append(i)
    func_starts.append(len(lines) + 1)  # end marker

    for i in range(len(func_starts) - 1):
        start = func_starts[i]
        end = func_starts[i + 1]
        length = end - start
        if length > threshold:
            findings.append(Finding(
                agent="static",
                rule_id="C201",
                message=f"Function length {length} lines exceeds {threshold}. Consider refactoring.",
                severity="warning",
                filepath=filepath,
                line=start,
                col=1
            ))
    return findings


# ------------------------------------
# Combine all complexity checks
# ------------------------------------
def run_complexity_checks(filepath: str, code: str):
    """
    Runs all complexity-related checks and returns findings.
    """
    findings = []
    findings += check_cyclomatic_complexity(filepath, code)
    findings += check_function_length(filepath, code)
    return findings

"""
Static Analysis — Style Rules
-----------------------------
This module implements basic linting rules similar to Flake8 or Pylint.
Checks include:
- Line length
- Function naming conventions
- Mutable default arguments
- Bare except statements
- Unused imports (basic)
"""

import re
from ..models import Finding

# -------------------------------
# Rule: Maximum line length
# -------------------------------
def check_line_length(filepath: str, code: str, max_len: int = 100):
    findings = []
    for i, line in enumerate(code.splitlines(), start=1):
        if len(line) > max_len:
            findings.append(Finding(
                agent="static",
                rule_id="S100",
                message=f"Line exceeds {max_len} characters",
                severity="warning",
                filepath=filepath,
                line=i,
                col=max_len + 1,
                code_snippet=line
            ))
    return findings


# -------------------------------
# Rule: Function names (snake_case)
# -------------------------------
SNAKE_CASE = re.compile(r"^[a-z_][a-z0-9_]*$")

def check_function_names(filepath: str, code: str):
    findings = []
    pattern = re.compile(r"^\\s*def\\s+([A-Za-z_][A-Za-z0-9_]*)\\s*\\(")
    for i, line in enumerate(code.splitlines(), start=1):
        match = pattern.search(line)
        if match:
            func_name = match.group(1)
            if not SNAKE_CASE.match(func_name):
                findings.append(Finding(
                    agent="static",
                    rule_id="S101",
                    message=f"Function '{func_name}' should follow snake_case naming",
                    severity="warning",
                    filepath=filepath,
                    line=i,
                    col=line.find(func_name) + 1,
                    code_snippet=line.strip()
                ))
    return findings


# -------------------------------
# Rule: Mutable default arguments
# -------------------------------
def check_mutable_defaults(filepath: str, code: str):
    findings = []
    # Detect functions with list/dict/set as default args
    pattern = re.compile(r"def\\s+\\w+\\s*\\([^)]*(=\\s*(\\[|\\{|set\\())")
    for i, line in enumerate(code.splitlines(), start=1):
        if pattern.search(line):
            findings.append(Finding(
                agent="static",
                rule_id="S104",
                message="Avoid mutable default arguments (use None and assign inside function).",
                severity="warning",
                filepath=filepath,
                line=i,
                col=1,
                code_snippet=line.strip()
            ))
    return findings


# -------------------------------
# Rule: Bare except clauses
# -------------------------------
def check_bare_except(filepath: str, code: str):
    findings = []
    for i, line in enumerate(code.splitlines(), start=1):
        if re.search(r"except\\s*:\\s*$", line.strip()):
            findings.append(Finding(
                agent="static",
                rule_id="S105",
                message="Avoid bare 'except:' — catch specific exceptions instead.",
                severity="warning",
                filepath=filepath,
                line=i,
                col=1,
                code_snippet=line.strip()
            ))
    return findings


# -------------------------------
# Rule: Unused imports (simple version)
# -------------------------------
def check_unused_imports(filepath: str, code: str):
    findings = []
    imports = []
    lines = code.splitlines()

    # Collect all imported names
    for i, line in enumerate(lines, start=1):
        match = re.match(r"\\s*import\\s+([A-Za-z0-9_]+)", line)
        if match:
            imports.append((match.group(1), i))

    # Check if they appear later
    for name, lineno in imports:
        if name not in code.split(name, 1)[-1]:  # crude check
            findings.append(Finding(
                agent="static",
                rule_id="S106",
                message=f"Imported module '{name}' appears unused.",
                severity="info",
                filepath=filepath,
                line=lineno,
                col=1,
                code_snippet=lines[lineno - 1].strip()
            ))
    return findings


# -------------------------------
# Combine all static checks
# -------------------------------
def run_style_rules(filepath: str, code: str):
    findings = []
    findings += check_line_length(filepath, code)
    findings += check_function_names(filepath, code)
    findings += check_mutable_defaults(filepath, code)
    findings += check_bare_except(filepath, code)
    findings += check_unused_imports(filepath, code)
    return findings

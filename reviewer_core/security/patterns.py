"""
Security Agent — Pattern Scanner
--------------------------------
This module uses regex-based scanning to detect common
security issues in Python code (e.g., eval, exec, os.system, SQL injection, etc.).
"""

import regex as re
from ..models import Finding

# ------------------------------------------------------
# Known dangerous or suspicious patterns
# ------------------------------------------------------
PATTERNS = [
    # Code execution / injection
    ("SEC001", r"\beval\s*\(", "Use of eval() is dangerous — consider ast.literal_eval or safer alternatives."),
    ("SEC002", r"\bexec\s*\(", "Use of exec() is unsafe — avoid dynamic code execution."),
    ("SEC003", r"\bos\.system\s*\(", "Use of os.system() can be unsafe with user input."),
    ("SEC004", r"\bsubprocess\.(Popen|run|call)\s*\(", "Subprocess call risk — use shell=False and sanitize inputs."),
    
    # SQL injection patterns
    ("SEC005", r"cursor\.execute\s*\(\s*f?['\"].*(SELECT|INSERT|UPDATE|DELETE).*['\"]", 
     "Possible raw SQL string detected — use parameterized queries."),
    
    # Serialization / deserialization
    ("SEC006", r"\bpickle\.(load|loads)\s*\(", "Insecure deserialization using pickle — may lead to RCE."),
    
    # Weak cryptography
    ("SEC007", r"\bhashlib\.(md5|sha1)\s*\(", "Weak hashing algorithm — use SHA-256 or bcrypt instead."),
    
    # Unsafe YAML load
    ("SEC008", r"yaml\.load\s*\(", "Unsafe YAML loading — use yaml.safe_load instead."),
    
    # Hardcoded secrets
    ("SEC009", r"(AKIA[0-9A-Z]{16})", "Possible AWS Access Key exposed."),
    
    # Potential command injections
    ("SEC010", r"\binput\s*\(", "User input detected — ensure it’s validated before usage."),
]

# ------------------------------------------------------
# Function: regex_scan
# ------------------------------------------------------
def regex_scan(filepath: str, code: str):
    """
    Scans code using regex for known security patterns.
    Returns a list of Finding objects for each detected issue.
    """
    findings = []
    for rule_id, pattern, message in PATTERNS:
        for match in re.finditer(pattern, code, flags=re.I):
            line = code.count("\n", 0, match.start()) + 1
            col = match.start() - (code.rfind("\n", 0, match.start()) + 1) + 1
            snippet = code.splitlines()[line - 1] if line <= len(code.splitlines()) else ""
            findings.append(Finding(
                agent="security",
                rule_id=rule_id,
                message=message,
                severity="warning",
                filepath=filepath,
                line=line,
                col=col,
                code_snippet=snippet.strip()
            ))
    return findings

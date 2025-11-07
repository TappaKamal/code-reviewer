"""
Security Agent
---------------
Scans Python code for potential security vulnerabilities,
including:
- Dangerous functions (eval, exec, os.system)
- SQL injection patterns
- Insecure serialization
- Weak cryptographic hashes
- Taint analysis for unsafe data flow
"""

from .runner import run_security

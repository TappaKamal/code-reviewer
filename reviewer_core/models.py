from dataclasses import dataclass
from typing import List, Optional, Literal, Dict, Any

# Define possible severity levels
Severity = Literal["info", "warning", "error"]

@dataclass
class Finding:
    """
    Represents a single issue or comment found by an agent.
    """
    agent: str                # e.g. "static", "security", "llm"
    rule_id: str              # e.g. "S101" or "SEC003"
    message: str              # Human-readable message
    severity: Severity        # info | warning | error
    filepath: str             # File being analyzed
    line: int                 # Line number where issue occurs
    col: int                  # Column number
    code_snippet: Optional[str] = None  # Offending code snippet
    suggestion: Optional[str] = None    # Suggested fix or improvement
    meta: Optional[Dict[str, Any]] = None  # Optional extra metadata

@dataclass
class ReviewBundle:
    """
    Stores the combined output of all three agents.
    """
    static_findings: List[Finding]
    security_findings: List[Finding]
    llm_comments: List[Finding]

"""
Code Review Orchestrator
------------------------
This module coordinates all agents:
1. Static Analysis Agent
2. Security Agent
3. LLM Reviewer Agent

It collects findings from each, merges them,
and returns a combined review bundle.
"""

from .static_analysis.runner import run_static
from .security.runner import run_security
from .llm.gemini_client import review_code
from .models import ReviewBundle


def review_file(filepath: str, code: str) -> ReviewBundle:
    """
    Run static analysis, security scanning, and LLM review
    for the provided code, returning a unified ReviewBundle.
    """
    print(f"📄 Reviewing file: {filepath}")

    # 1️⃣ Static Analysis
    print("🔍 Running Static Analysis...")
    static_findings = run_static(filepath, code)
    print(f"✅ Static analysis completed — {len(static_findings)} issues found.")

    # 2️⃣ Security Analysis
    print("🛡️ Running Security Analysis...")
    security_findings = run_security(filepath, code)
    print(f"✅ Security scan completed — {len(security_findings)} warnings found.")

    # 3️⃣ LLM Review
    print("🤖 Requesting LLM review from Gemini...")
    llm_comments = review_code(filepath, code, static_findings, security_findings)
    print("✅ LLM review completed.")

    # 4️⃣ Combine everything
    bundle = ReviewBundle(
        static_findings=static_findings,
        security_findings=security_findings,
        llm_comments=llm_comments,
    )

    print("\n📦 All agents finished successfully.\n")
    return bundle

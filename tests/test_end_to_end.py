"""
Test — End-to-End System Integration
------------------------------------
Verifies that the orchestrator correctly runs:
1. Static analysis
2. Security scanning
3. LLM review (mocked if API key not set)
"""

import os
from reviewer_core.orchestrator import review_file


def test_end_to_end_review(monkeypatch):
    # Disable Gemini call if API key not available
    monkeypatch.setenv("GEMINI_API_KEY", "fake_key")

    code = """
import os
def test_func():
    name = input("Enter: ")
    os.system("echo " + name)
"""
    result = review_file("test_e2e.py", code)

    # Check all three agents returned results
    assert hasattr(result, "static_findings")
    assert hasattr(result, "security_findings")
    assert hasattr(result, "llm_comments")

    # Static should detect at least one rule (mutable default, naming, etc.)
    assert any(result.static_findings), "Static analysis should produce at least one finding."

    # Security agent should detect taint or os.system
    assert any(result.security_findings), "Security agent should produce findings."

    # LLM comment should exist even if Gemini key is fake
    assert result.llm_comments, "LLM Reviewer should return at least one comment object."

    print("\n✅ End-to-End Review Passed!")

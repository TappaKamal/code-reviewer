"""
LLM Reviewer — Gemini Client
----------------------------
This module connects to the Google Gemini API and
uses the SYSTEM and USER prompts to produce
natural-language code reviews with contextual awareness.
"""

import os
import google.generativeai as genai
from ..models import Finding
from .prompts import SYSTEM_STYLE, USER_TEMPLATE


def review_code(filepath: str, code: str, static_findings, security_findings):
    """
    Use Gemini to perform a natural-language code review.

    Args:
        filepath (str): Path to file being reviewed.
        code (str): The Python code content.
        static_findings (list[Finding]): Style & complexity issues.
        security_findings (list[Finding]): Security issues.

    Returns:
        list[Finding]: One or more LLM-generated review comments.
    """
    # Configure Gemini
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    model = genai.GenerativeModel(model_name)

    # Condense static/security findings for LLM context
    condensed = "\n".join(
        f"- [{f.severity.upper()}] {f.rule_id} (L{f.line}): {f.message}"
        for f in (static_findings + security_findings)[:40]
    ) or "(No issues detected by automated agents.)"

    # Create the full user prompt
    prompt = USER_TEMPLATE.format(
        filepath=filepath,
        condensed_findings=condensed,
        code=code[:16000]  # limit for large files
    )

    # Combine system and user prompts
    print("🤖 Sending code to Gemini for review...")

    try:
        response = model.generate_content([SYSTEM_STYLE, prompt])
        text = response.text or "(No response from Gemini)"
    except Exception as e:
        text = f"⚠️ Gemini API error: {e}"

    # Wrap LLM output in Finding format
    llm_finding = Finding(
        agent="llm",
        rule_id="LLM000",
        message=text.strip(),
        severity="info",
        filepath=filepath,
        line=1,
        col=1,
    )

    return [llm_finding]

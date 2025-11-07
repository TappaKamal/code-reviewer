"""
LLM Reviewer Agent
------------------
Uses Gemini API to generate human-like code review feedback.
Combines static and security analysis context to produce
natural, professional review comments and refactor suggestions.
"""

from .gemini_client import review_code

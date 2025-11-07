"""
LLM Reviewer — Prompt Templates
-------------------------------
This file defines the system and user prompt templates
for the Gemini LLM. These prompts control the tone,
structure, and level of detail of AI-generated code reviews.
"""

SYSTEM_STYLE = """
You are a senior Python code reviewer.
Your goals:
- Be concise, accurate, and professional.
- Identify style, performance, and security issues.
- Suggest clear, actionable fixes.
- Prefer examples and short refactor suggestions.
- Use markdown formatting where possible.
"""

USER_TEMPLATE = """
File: {filepath}

Static & Security Findings (context for you):
{condensed_findings}

Code to review:
```python
{code}

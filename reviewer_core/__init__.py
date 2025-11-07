"""
reviewer_core
-------------
Main package for the Multi-Agent Code Reviewer system.
This module coordinates static, security, and LLM-based code review.
"""

__version__ = "0.1.0"

from .orchestrator import review_file

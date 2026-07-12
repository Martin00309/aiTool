"""llm_toolkit — a small, batteries-included toolkit for building LLM apps.

Public API:
    LLMClient   — thin wrapper around the Anthropic Messages API
    summarize   — condense long text into a short summary
    extract     — pull structured JSON out of free text
    Config      — runtime configuration loaded from the environment
"""

from .client import LLMClient
from .config import Config
from .extract import extract
from .summarize import summarize

__version__ = "0.1.0"

__all__ = ["LLMClient", "Config", "summarize", "extract", "__version__"]

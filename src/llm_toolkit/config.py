"""Runtime configuration, loaded from environment variables.

Reading configuration in one place keeps API keys and model names out of the
rest of the codebase and makes the app easy to reconfigure without code changes.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

# Default model. Swap via the MODEL env var. Valid strings as of mid-2026 include:
#   claude-sonnet-4-6  (balanced default)
#   claude-sonnet-5    (newer, near-Opus quality)
#   claude-opus-4-8    (maximum reasoning)
#   claude-haiku-4-5   (fastest / cheapest)
#   claude-fable-5     (frontier)
DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_MAX_TOKENS = 1024


@dataclass(frozen=True)
class Config:
    """Immutable app configuration."""

    api_key: str
    model: str = DEFAULT_MODEL
    max_tokens: int = DEFAULT_MAX_TOKENS

    @classmethod
    def from_env(cls) -> "Config":
        """Build a Config from environment variables.

        Reads (optionally from a local .env file if python-dotenv is installed):
            ANTHROPIC_API_KEY  (required)
            MODEL              (optional)
            MAX_TOKENS         (optional)

        Raises:
            RuntimeError: if ANTHROPIC_API_KEY is missing.
        """
        # Load a .env file if python-dotenv is available. It is an optional
        # convenience for local development and never required in production.
        try:
            from dotenv import load_dotenv

            load_dotenv()
        except ImportError:
            pass

        api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add "
                "your key, or export it: export ANTHROPIC_API_KEY=sk-ant-..."
            )

        model = os.getenv("MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL

        raw_max = os.getenv("MAX_TOKENS", "").strip()
        try:
            max_tokens = int(raw_max) if raw_max else DEFAULT_MAX_TOKENS
        except ValueError:
            max_tokens = DEFAULT_MAX_TOKENS

        return cls(api_key=api_key, model=model, max_tokens=max_tokens)

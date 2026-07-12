"""A thin, friendly wrapper around the Anthropic Messages API.

The wrapper exists so the rest of the app talks to one small, stable surface
(`complete`, `stream`) instead of the full SDK. That makes the code easier to
test and easier to point at a different backend later.
"""

from __future__ import annotations

from collections.abc import Iterator

from .config import Config


class LLMClient:
    """Wraps an Anthropic client and exposes two simple methods."""

    def __init__(self, config: Config | None = None) -> None:
        # Import here so that importing the package doesn't require the SDK to be
        # installed (useful for tests that never make a network call).
        import anthropic

        self.config = config or Config.from_env()
        self._client = anthropic.Anthropic(api_key=self.config.api_key)

    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Send a single prompt and return the model's text response.

        Args:
            prompt:     The user message.
            system:     Optional system prompt to steer behavior.
            max_tokens: Override the configured output-token cap.

        Returns:
            The concatenated text of the response.
        """
        kwargs: dict = {
            "model": self.config.model,
            "max_tokens": max_tokens or self.config.max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            kwargs["system"] = system

        response = self._client.messages.create(**kwargs)
        return _text_of(response)

    def stream(
        self,
        prompt: str,
        *,
        system: str | None = None,
        max_tokens: int | None = None,
    ) -> Iterator[str]:
        """Stream a response, yielding text chunks as they arrive.

        Useful for a responsive CLI or UI where you want to print tokens live.
        """
        kwargs: dict = {
            "model": self.config.model,
            "max_tokens": max_tokens or self.config.max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            kwargs["system"] = system

        with self._client.messages.stream(**kwargs) as stream:
            yield from stream.text_stream


def _text_of(response) -> str:
    """Extract plain text from a Messages API response.

    A response's `content` is a list of blocks; we keep only the text blocks and
    join them, which is robust even when the model returns multiple blocks.
    """
    parts = [block.text for block in response.content if getattr(block, "type", None) == "text"]
    return "".join(parts).strip()

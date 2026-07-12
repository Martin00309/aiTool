"""Summarize free text into a short, faithful summary."""

from __future__ import annotations

from .client import LLMClient

_SYSTEM = (
    "You are a precise summarizer. Produce a faithful summary that keeps the "
    "key facts and omits filler. Do not add information that is not present in "
    "the source text."
)


def summarize(
    text: str,
    *,
    sentences: int = 3,
    client: LLMClient | None = None,
) -> str:
    """Summarize ``text`` in roughly ``sentences`` sentences.

    Args:
        text:      The source text to condense.
        sentences: Target length of the summary, in sentences.
        client:    An optional pre-built client (handy for tests / reuse).

    Returns:
        The summary as a string.
    """
    if not text.strip():
        return ""

    client = client or LLMClient()
    prompt = (
        f"Summarize the text below in about {sentences} sentence(s).\n\n"
        f"---\n{text}\n---"
    )
    return client.complete(prompt, system=_SYSTEM)

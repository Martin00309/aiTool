"""Extract structured data from unstructured text as JSON.

This demonstrates a common, practical LLM pattern: ask the model to return
*only* JSON matching a set of fields, then parse it safely on the client.
"""

from __future__ import annotations

import json
import re
from typing import Any

from .client import LLMClient

_SYSTEM = (
    "You are a careful information-extraction engine. Respond with a single "
    "valid JSON object and nothing else — no prose, no markdown, no code fences. "
    "Use null for any requested field you cannot find in the text."
)


def extract(
    text: str,
    fields: list[str],
    *,
    client: LLMClient | None = None,
) -> dict[str, Any]:
    """Extract the requested ``fields`` from ``text`` into a dict.

    Args:
        text:   Source text to read.
        fields: Field names to populate (e.g. ["name", "email", "company"]).
        client: Optional pre-built client.

    Returns:
        A dict keyed by the requested field names. Missing values are ``None``.

    Raises:
        ValueError: if the model's response cannot be parsed as JSON.
    """
    if not fields:
        raise ValueError("`fields` must contain at least one field name.")

    client = client or LLMClient()
    field_list = ", ".join(fields)
    prompt = (
        f"Extract these fields as JSON keys: {field_list}.\n\n"
        f"Text:\n---\n{text}\n---"
    )
    raw = client.complete(prompt, system=_SYSTEM)
    data = _parse_json(raw)

    # Normalize: guarantee every requested field is present.
    return {field: data.get(field) for field in fields}


def _parse_json(raw: str) -> dict[str, Any]:
    """Parse JSON from a model response, tolerating stray code fences."""
    cleaned = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model did not return valid JSON: {raw!r}") from exc

    if not isinstance(result, dict):
        raise ValueError(f"Expected a JSON object, got: {type(result).__name__}")
    return result

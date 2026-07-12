"""Tests for extract() and summarize() using a fake client — no network calls.

Because both functions accept a `client` argument, we can inject a stub that
returns canned responses. This keeps the tests fast, free, and deterministic.
"""

import pytest

from llm_toolkit.extract import _parse_json, extract
from llm_toolkit.summarize import summarize


class FakeClient:
    """Stand-in for LLMClient that returns a preset response."""

    def __init__(self, response: str):
        self.response = response
        self.last_prompt = None
        self.last_system = None

    def complete(self, prompt, *, system=None, max_tokens=None):
        self.last_prompt = prompt
        self.last_system = system
        return self.response


def test_extract_returns_requested_fields():
    fake = FakeClient('{"name": "Ada Lovelace", "role": "mathematician"}')
    result = extract("Ada Lovelace was a mathematician.", ["name", "role"], client=fake)
    assert result == {"name": "Ada Lovelace", "role": "mathematician"}


def test_extract_fills_missing_fields_with_none():
    fake = FakeClient('{"name": "Ada Lovelace"}')
    result = extract("Ada Lovelace.", ["name", "email"], client=fake)
    assert result == {"name": "Ada Lovelace", "email": None}


def test_extract_strips_code_fences():
    fake = FakeClient('```json\n{"name": "Ada"}\n```')
    result = extract("Ada.", ["name"], client=fake)
    assert result == {"name": "Ada"}


def test_extract_rejects_empty_fields():
    fake = FakeClient("{}")
    with pytest.raises(ValueError):
        extract("text", [], client=fake)


def test_extract_raises_on_bad_json():
    fake = FakeClient("this is not json")
    with pytest.raises(ValueError, match="valid JSON"):
        extract("text", ["name"], client=fake)


def test_summarize_empty_text_short_circuits():
    # No client needed — empty input returns "" without any call.
    assert summarize("   ") == ""


def test_summarize_passes_text_to_client():
    fake = FakeClient("A short summary.")
    result = summarize("A long piece of text.", sentences=1, client=fake)
    assert result == "A short summary."
    assert "A long piece of text." in fake.last_prompt


def test_parse_json_object_only():
    with pytest.raises(ValueError, match="JSON object"):
        _parse_json("[1, 2, 3]")

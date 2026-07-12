"""Tests for configuration loading. These run offline — no API calls."""

import pytest

from llm_toolkit.config import DEFAULT_MAX_TOKENS, DEFAULT_MODEL, Config


def test_from_env_reads_key(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    monkeypatch.delenv("MODEL", raising=False)
    monkeypatch.delenv("MAX_TOKENS", raising=False)

    config = Config.from_env()

    assert config.api_key == "sk-ant-test"
    assert config.model == DEFAULT_MODEL
    assert config.max_tokens == DEFAULT_MAX_TOKENS


def test_from_env_missing_key_raises(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        Config.from_env()


def test_from_env_overrides(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    monkeypatch.setenv("MODEL", "claude-opus-4-8")
    monkeypatch.setenv("MAX_TOKENS", "2048")

    config = Config.from_env()

    assert config.model == "claude-opus-4-8"
    assert config.max_tokens == 2048


def test_invalid_max_tokens_falls_back(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    monkeypatch.setenv("MAX_TOKENS", "not-a-number")

    config = Config.from_env()

    assert config.max_tokens == DEFAULT_MAX_TOKENS

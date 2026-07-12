"""Command-line interface for llm_toolkit.

Usage examples:
    llm-toolkit summarize examples/sample_article.txt --sentences 2
    cat notes.txt | llm-toolkit summarize -
    llm-toolkit extract examples/sample_article.txt --fields title,author,topic
    llm-toolkit chat
"""

from __future__ import annotations

import argparse
import json
import sys

from .chat import run_chat
from .client import LLMClient
from .config import Config
from .extract import extract
from .summarize import summarize


def _read_source(path: str) -> str:
    """Read text from a file path, or from stdin when path is '-'."""
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="llm-toolkit",
        description="A small toolkit for LLM-powered text tasks.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_sum = sub.add_parser("summarize", help="Summarize a text file (or '-' for stdin).")
    p_sum.add_argument("source", help="Path to a text file, or '-' to read stdin.")
    p_sum.add_argument("--sentences", type=int, default=3, help="Target summary length.")

    p_ext = sub.add_parser("extract", help="Extract structured JSON fields from text.")
    p_ext.add_argument("source", help="Path to a text file, or '-' to read stdin.")
    p_ext.add_argument(
        "--fields",
        required=True,
        help="Comma-separated field names, e.g. title,author,topic",
    )

    sub.add_parser("chat", help="Start an interactive chat session.")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point. Returns a process exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        config = Config.from_env()
    except RuntimeError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2

    client = LLMClient(config)

    if args.command == "summarize":
        text = _read_source(args.source)
        print(summarize(text, sentences=args.sentences, client=client))
        return 0

    if args.command == "extract":
        text = _read_source(args.source)
        fields = [f.strip() for f in args.fields.split(",") if f.strip()]
        result = extract(text, fields, client=client)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    if args.command == "chat":
        run_chat(client)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

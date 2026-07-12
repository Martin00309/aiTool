"""Minimal programmatic example.

Run from the project root after installing (`pip install -e .`) and setting
ANTHROPIC_API_KEY:

    python examples/quickstart.py
"""

from pathlib import Path

from llm_toolkit import LLMClient, extract, summarize


def main() -> None:
    article = Path(__file__).parent.joinpath("sample_article.txt").read_text(encoding="utf-8")

    # Reuse a single client across calls.
    client = LLMClient()

    print("=== Summary ===")
    print(summarize(article, sentences=2, client=client))

    print("\n=== Extracted fields ===")
    fields = extract(article, ["title", "author", "main_topic"], client=client)
    for key, value in fields.items():
        print(f"{key}: {value}")

    print("\n=== One-off completion ===")
    print(client.complete("Give me one tip for writing clear prompts."))


if __name__ == "__main__":
    main()

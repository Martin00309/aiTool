"""A minimal streaming chat REPL that keeps conversation history.

The API is stateless, so we resend the full message history on every turn. This
module shows the smallest correct way to hold a multi-turn conversation.
"""

from __future__ import annotations

from .client import LLMClient

_SYSTEM = "You are a concise, helpful assistant."


def run_chat(client: LLMClient | None = None) -> None:
    """Start an interactive chat loop. Type 'exit' or Ctrl-C to quit."""
    import anthropic

    client = client or LLMClient()
    history: list[dict[str, str]] = []

    print("Chat started. Type 'exit' to quit.\n")
    while True:
        try:
            user_input = input("you › ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return

        if user_input.lower() in {"exit", "quit"}:
            print("Bye!")
            return
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        print("bot › ", end="", flush=True)
        reply_parts: list[str] = []
        # Access the underlying SDK client for full multi-turn history.
        with client._client.messages.stream(
            model=client.config.model,
            max_tokens=client.config.max_tokens,
            system=_SYSTEM,
            messages=history,
        ) as stream:
            for chunk in stream.text_stream:
                print(chunk, end="", flush=True)
                reply_parts.append(chunk)
        print("\n")

        history.append({"role": "assistant", "content": "".join(reply_parts)})

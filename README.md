# LLM Text Toolkit

A small, batteries-included Python project that shows how to build practical
LLM-powered features. It wraps a large language model (Anthropic's Claude) behind
a clean, testable API and ships with a command-line interface, examples, and
tests.

Use it as a starting template for your own AI apps, or as a reference for common
patterns: a thin client wrapper, prompt design, structured (JSON) output,
streaming, config via environment variables, and testing LLM code without making
real API calls.

## Features

- **Summarize** — condense long text into a short, faithful summary.
- **Extract** — pull structured JSON fields out of unstructured text.
- **Chat** — an interactive, streaming, multi-turn REPL.
- **Clean library API** — call `summarize()`, `extract()`, and `LLMClient` from your own code.
- **Testable design** — functions accept an injectable client, so tests run offline with no API key.

## Project structure

```
llm-text-toolkit/
├── README.md
├── LICENSE
├── pyproject.toml          # packaging + CLI entry point
├── requirements.txt
├── .env.example            # copy to .env and add your key
├── .gitignore
├── src/
│   └── llm_toolkit/
│       ├── __init__.py     # public API
│       ├── config.py       # loads settings from the environment
│       ├── client.py       # thin wrapper around the Anthropic API
│       ├── summarize.py    # summarization
│       ├── extract.py      # structured JSON extraction
│       ├── chat.py         # streaming chat REPL
│       └── cli.py          # command-line interface
├── examples/
│   ├── sample_article.txt
│   └── quickstart.py       # programmatic usage
└── tests/
    ├── test_config.py
    └── test_extract.py     # offline tests using a fake client
```

## Requirements

- Python 3.9 or newer
- An Anthropic API key ([get one here](https://console.anthropic.com/))

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/llm-text-toolkit.git
cd llm-text-toolkit

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate

# 3. Install the package (editable) with dev extras
pip install -e ".[dev]"
```

## Configuration

Copy the example environment file and add your key:

```bash
cp .env.example .env
# then edit .env and set ANTHROPIC_API_KEY
```

Or export it directly in your shell:

```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

| Variable            | Required | Default              | Description                        |
| ------------------- | -------- | -------------------- | ---------------------------------- |
| `ANTHROPIC_API_KEY` | yes      | —                    | Your Anthropic API key.            |
| `MODEL`             | no       | `claude-sonnet-4-6`  | Which model to call.               |
| `MAX_TOKENS`        | no       | `1024`               | Max output tokens per response.    |

Other valid model strings include `claude-sonnet-5`, `claude-opus-4-8`,
`claude-haiku-4-5`, and `claude-fable-5`. Check the
[official model docs](https://docs.claude.com/en/docs/about-claude/models/overview)
for the current list.

## Usage

### Command line

```bash
# Summarize a file (or read from stdin with "-")
llm-toolkit summarize examples/sample_article.txt --sentences 2
cat notes.txt | llm-toolkit summarize -

# Extract structured JSON fields
llm-toolkit extract examples/sample_article.txt --fields title,author,main_topic

# Interactive chat (type "exit" to quit)
llm-toolkit chat
```

### As a library

```python
from llm_toolkit import LLMClient, summarize, extract

client = LLMClient()

# Summarize
print(summarize("...long text...", sentences=3, client=client))

# Extract structured data
data = extract("Jane Doe, jane@example.com, Acme Corp", ["name", "email", "company"])
print(data)   # {'name': 'Jane Doe', 'email': 'jane@example.com', 'company': 'Acme Corp'}

# One-off completion
print(client.complete("Explain recursion in one sentence."))

# Stream a response token by token
for chunk in client.stream("Write a haiku about the sea."):
    print(chunk, end="", flush=True)
```

There is also a runnable end-to-end example:

```bash
python examples/quickstart.py
```

## Running the tests

The test suite runs **offline** — it injects a fake client, so no API key or
network access is needed:

```bash
pytest
```

## How it works

- **`config.py`** reads settings once, from the environment, and validates them.
  Keeping this in one place keeps secrets and model names out of the rest of the
  code.
- **`client.py`** wraps the Anthropic Messages API in two small methods,
  `complete()` and `stream()`. The rest of the app depends on this narrow
  surface rather than the full SDK, which makes it easy to test and to swap
  backends later.
- **`extract.py`** shows a reliable structured-output pattern: instruct the model
  to return JSON only, then parse it defensively on the client (tolerating stray
  code fences and guaranteeing every requested field is present).
- Because `summarize()` and `extract()` accept an optional `client`, tests pass
  in a stub that returns canned responses — no real calls required.

## Extending it

Some natural next steps:

- Add a `translate` or `classify` command following the same pattern.
- Add retries with backoff around API calls in `client.py`.
- Ground answers in your own documents (retrieval) before calling the model.
- Wrap the library in a small web API (FastAPI) or UI.

## License

Released under the [MIT License](LICENSE).

---

_This project is an independent example and is not affiliated with or endorsed by Anthropic._
# aiTool


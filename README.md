# git-camus

Craft Git commit messages with existential flair using [Ollama](https://ollama.com), [OpenAI](https://platform.openai.com/), [Claude](https://docs.anthropic.com/), or the [Claude CLI](https://docs.claude.com/en/docs/claude-code).

git-camus analyzes your staged changes and generates philosophical commit messages inspired by Albert Camus — reflecting on the absurdity, rebellion, and human condition behind every diff.

## Prerequisites

- Python 3.9+
- One of the following LLM providers:
  - **Ollama** (default) — running locally or accessible via network, with a pulled model (default: `llama3.2`)
  - **OpenAI** — an API key with access to chat completions (default model: `gpt-4o-mini`)
  - **Claude** — an Anthropic API key (default model: `claude-sonnet-4-20250514`)
  - **Claude CLI** — a locally-installed Claude CLI with active login (no API key required)

## Installation

```bash
pip install git-camus
```

Or install as a standalone utility into a specific directory:

```bash
git clone https://github.com/rachlenko/git-camus.git
cd git-camus
./install.sh --prefix /usr/local
```

This creates an isolated virtual environment under `PREFIX/lib/git-camus/` and places the `git-camus` executable in `PREFIX/bin/`. The default prefix is `/usr/local`.

```bash
# Install to a custom location
./install.sh --prefix ~/.local

# Install system-wide (may require sudo)
sudo ./install.sh --prefix /usr/local
```

Or install directly with pip:

```bash
pip install .
```

For development:

```bash
pip install -e ".[dev]"
```

## Usage

Stage your changes, then run:

```bash
git-camus
```

### Options

| Flag | Description |
|------|-------------|
| `--show`, `-s` | Preview the generated message without committing |
| `--message`, `-m` | Provide context to guide the philosophical reflection |
| `--provider`, `-p` | LLM provider: `ollama` (default), `openai`, `claude`, or `claude-cli` |

### Examples

```bash
# Generate and commit using Ollama (default)
git add .
git-camus

# Preview without committing
git-camus --show

# Provide context
git-camus -m "fixed auth token expiry"

# Use OpenAI
export OPENAI_API_KEY="sk-..."
git-camus --provider openai

# Use Claude
export ANTHROPIC_API_KEY="sk-ant-..."
git-camus --provider claude

# Set the default provider via environment variable
export GIT_CAMUS_PROVIDER=claude
git-camus
```

## Configuration

### Ollama (default provider)

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama API endpoint |
| `OLLAMA_MODEL` | `llama3.2` | Model to use for generation |

### OpenAI

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *(required)* | OpenAI API key |
| `OPENAI_API_HOST` | `https://api.openai.com/v1` | OpenAI-compatible API endpoint |
| `OPENAI_MODEL` | `gpt-4o-mini` | Model to use for generation |

### Claude

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | *(required)* | Anthropic API key |
| `ANTHROPIC_API_HOST` | `https://api.anthropic.com` | Anthropic-compatible API endpoint |
| `ANTHROPIC_MODEL` | `claude-sonnet-4-20250514` | Model to use for generation |

### `claude-cli` provider

Generate the message with your locally-installed **Claude CLI** (`claude -p`),
using the CLI's own login — **no `ANTHROPIC_API_KEY` required**:

```bash
git-camus -p claude-cli            # or: GIT_CAMUS_PROVIDER=claude-cli git-camus
```

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_CAMUS_CLAUDE_CLI_BIN` | `claude` | Path to the Claude CLI binary |

Requires the `claude` CLI on your `PATH` and logged in. Unlike the `claude` provider (Anthropic HTTP API,
needs a key), `claude-cli` strips `ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN` so
the CLI authenticates the same way it does when you run it directly.

### General

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_CAMUS_PROVIDER` | `ollama` | Default provider (`ollama`, `openai`, `claude`, or `claude-cli`) |

The `OPENAI_API_HOST` and `ANTHROPIC_API_HOST` variables allow using any compatible API proxy or gateway.

## License

[MIT](LICENSE)

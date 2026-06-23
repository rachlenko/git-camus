#!/usr/bin/env python3
"""Generate philosophical Git commit messages inspired by Albert Camus using Ollama, OpenAI, or Claude."""

__version__ = "0.5.0"

import os
import subprocess
import sys
from typing import Any, Optional, TypedDict

import click
import httpx

MAX_DIFF_LENGTH = 8000

PROVIDERS = ("ollama", "openai", "claude", "claude-cli")

DEFAULT_SYSTEM_PROMPT = (
    "You are an AI assistant that generates philosophical commit messages in the style of Albert Camus. "
    "Your task is to analyze git changes and create a commit message that reflects on the absurdity, rebellion, and human condition."
)

DEFAULT_USER_PROMPT = (
    "Git Diff:\n{diff}\n\nGit Status:\n{status}\n\n"
    "Generate a philosophical commit message that:\n"
    "1. Reflects on the nature of the changes made\n"
    "2. Incorporates themes of existentialism and the absurd\n"
    "3. Is concise but meaningful (max 150 characters)\n"
    "4. Avoids technical jargon in favor of philosophical reflection\n\n"
    "Respond with only the commit message, no explanations or additional text."
)

DEFAULT_PROMPT = DEFAULT_SYSTEM_PROMPT + "\n\n" + DEFAULT_USER_PROMPT

DEFAULT_OLLAMA_HOST = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "llama3.2"
DEFAULT_OPENAI_HOST = "https://api.openai.com/v1"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_CLAUDE_HOST = "https://api.anthropic.com"
DEFAULT_CLAUDE_MODEL = "claude-sonnet-4-20250514"


class ChatMessage(TypedDict):
    role: str
    content: str


def get_git_diff() -> str:
    try:
        return subprocess.check_output(
            ["git", "diff", "--cached"], text=True, stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError:
        return ""


def get_git_status() -> str:
    try:
        return subprocess.check_output(
            ["git", "status", "--porcelain"], text=True, stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError:
        return ""


def perform_git_commit(message: str) -> None:
    try:
        subprocess.run(["git", "commit", "-m", message], check=True, text=True)
        click.echo(f"Committed with message: {message}")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error committing: {e}", err=True)
        sys.exit(1)


def resolve_provider() -> str:
    provider = os.environ.get("GIT_CAMUS_PROVIDER", "ollama").lower()
    if provider not in PROVIDERS:
        click.echo(f"Error: unknown provider '{provider}'. Use one of: {', '.join(PROVIDERS)}", err=True)
        sys.exit(1)
    return provider


def get_config_values(provider: str) -> tuple[str, str, str, Optional[str]]:
    """Return (host, model, prompt, api_key) for the chosen provider."""
    try:
        from core.config import settings
        prompt_message = settings.run.prompt_message
    except Exception:
        prompt_message = DEFAULT_PROMPT

    if provider == "claude":
        host = os.environ.get("ANTHROPIC_API_HOST", DEFAULT_CLAUDE_HOST)
        model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_CLAUDE_MODEL)
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            click.echo("Error: ANTHROPIC_API_KEY environment variable is required for claude provider", err=True)
            sys.exit(1)
        return host, model, prompt_message, api_key

    if provider == "claude-cli":
        # The claude CLI authenticates via its own login; no host/model/key here.
        return "", "", prompt_message, None

    if provider == "openai":
        host = os.environ.get("OPENAI_API_HOST", DEFAULT_OPENAI_HOST)
        model = os.environ.get("OPENAI_MODEL", DEFAULT_OPENAI_MODEL)
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            click.echo("Error: OPENAI_API_KEY environment variable is required for openai provider", err=True)
            sys.exit(1)
        return host, model, prompt_message, api_key

    host = os.environ.get("OLLAMA_HOST", DEFAULT_OLLAMA_HOST)
    model = os.environ.get("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
    try:
        from core.config import settings
        host = os.environ.get("OLLAMA_HOST", settings.ollama.host)
        model = os.environ.get("OLLAMA_MODEL", settings.run.model_name)
    except Exception:
        pass
    return host, model, prompt_message, None


def build_messages(diff: str, status: str, prompt_template: str, context_message: Optional[str] = None) -> list[ChatMessage]:
    if len(diff) > MAX_DIFF_LENGTH:
        diff = diff[:MAX_DIFF_LENGTH] + "\n... (truncated)"
    prompt = prompt_template.format(diff=diff, status=status)
    messages: list[ChatMessage] = [{"role": "user", "content": prompt}]
    if context_message:
        messages.append({
            "role": "user",
            "content": f"Original commit message context: {context_message}\n\nPlease consider this context when generating the philosophical reflection.",
        })
    return messages


def call_ollama(host: str, model: str, messages: list[ChatMessage]) -> str:
    request_data = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.7, "top_p": 0.9, "max_tokens": 150},
    }
    try:
        click.echo("Sending request to Ollama API...", err=True)
        response = httpx.post(f"{host}/api/chat", json=request_data, timeout=120.0)
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "").strip()
    except httpx.ConnectError:
        click.echo(f"Could not connect to Ollama at {host}", err=True)
        click.echo("Make sure Ollama is running and the host/port is correct", err=True)
        sys.exit(1)
    except httpx.HTTPError as e:
        click.echo(f"Ollama API error: {e}", err=True)
        sys.exit(1)


def call_openai(host: str, model: str, messages: list[ChatMessage], api_key: str) -> str:
    request_data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 150,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    try:
        click.echo("Sending request to OpenAI API...", err=True)
        response = httpx.post(f"{host}/chat/completions", json=request_data, headers=headers, timeout=120.0)
        response.raise_for_status()
        choices = response.json().get("choices", [])
        if not choices:
            return ""
        return choices[0].get("message", {}).get("content", "").strip()
    except httpx.ConnectError:
        click.echo(f"Could not connect to OpenAI API at {host}", err=True)
        sys.exit(1)
    except httpx.HTTPError as e:
        click.echo(f"OpenAI API error: {e}", err=True)
        sys.exit(1)


def call_claude(host: str, model: str, messages: list[ChatMessage], api_key: str) -> str:
    user_content = "\n\n".join(m["content"] for m in messages)
    request_data = {
        "model": model,
        "max_tokens": 256,
        "system": DEFAULT_SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": user_content}],
    }
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    try:
        click.echo("Sending request to Claude API...", err=True)
        response = httpx.post(f"{host}/v1/messages", json=request_data, headers=headers, timeout=120.0)
        response.raise_for_status()
        content_blocks = response.json().get("content", [])
        if not content_blocks:
            return ""
        return content_blocks[0].get("text", "").strip()
    except httpx.ConnectError:
        click.echo(f"Could not connect to Claude API at {host}", err=True)
        sys.exit(1)
    except httpx.HTTPError as e:
        click.echo(f"Claude API error: {e}", err=True)
        sys.exit(1)


def _strip_code_fences(text: str) -> str:
    t = text.strip()
    if t.startswith("```") and t.endswith("```"):
        lines = t.splitlines()
        if len(lines) >= 2:
            # Drop the opening fence (``` or ```lang) and the closing fence.
            lines = lines[1:-1]
        return "\n".join(lines).strip()
    return t


def call_claude_cli(messages: list[ChatMessage], binary: Optional[str] = None) -> str:
    prompt = DEFAULT_SYSTEM_PROMPT + "\n\n" + "\n\n".join(m["content"] for m in messages)
    binary = binary or os.environ.get("GIT_CAMUS_CLAUDE_CLI_BIN", "claude")
    # Drop API-key env so the claude CLI uses its own login (the same way it
    # authenticates when run directly), not an ANTHROPIC_API_KEY.
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")}
    try:
        click.echo("Generating commit message via 'claude -p'...", err=True)
        result = subprocess.run(
            [binary, "-p", prompt], capture_output=True, text=True, timeout=120, env=env
        )
    except FileNotFoundError:
        click.echo(
            f"Error: '{binary}' CLI not found on PATH (claude-cli provider needs the Claude CLI)",
            err=True,
        )
        sys.exit(1)
    except subprocess.TimeoutExpired:
        click.echo("Error: 'claude -p' timed out", err=True)
        sys.exit(1)
    if result.returncode != 0:
        click.echo(f"Error: 'claude -p' failed: {result.stderr.strip()}", err=True)
        sys.exit(1)
    return _strip_code_fences(result.stdout)


def run_git_camus(show: bool = False, message: Optional[str] = None, provider: Optional[str] = None) -> None:
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True
        )
    except subprocess.CalledProcessError:
        click.echo("Error: Not in a git repository", err=True)
        sys.exit(1)

    status = get_git_status()
    diff = get_git_diff()

    if not status.strip():
        click.echo("No staged changes to commit.", err=True)
        sys.exit(0)

    if provider is None:
        provider = resolve_provider()

    host, model, prompt_template, api_key = get_config_values(provider)
    messages = build_messages(diff, status, prompt_template, message)

    if provider == "claude":
        commit_message = call_claude(host, model, messages, api_key)  # type: ignore[arg-type]
    elif provider == "claude-cli":
        commit_message = call_claude_cli(messages)
    elif provider == "openai":
        commit_message = call_openai(host, model, messages, api_key)  # type: ignore[arg-type]
    else:
        commit_message = call_ollama(host, model, messages)

    if not commit_message:
        click.echo("Error: No commit message generated", err=True)
        sys.exit(1)

    if show:
        click.echo(commit_message)
    else:
        perform_git_commit(commit_message)


@click.command()
@click.option("--show", "-s", is_flag=True, help="Show the generated message without committing")
@click.option(
    "--message", "-m", help="Original commit message to enhance with Camus-style existentialism"
)
@click.option(
    "--provider", "-p", type=click.Choice(PROVIDERS, case_sensitive=False), default=None,
    help="LLM provider to use (default: ollama, or GIT_CAMUS_PROVIDER env var)",
)
def main(show: bool, message: Optional[str], provider: Optional[str]) -> None:
    """Generate an existential commit message in the style of Albert Camus."""
    run_git_camus(show=show, message=message, provider=provider)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate philosophical Git commit messages inspired by Albert Camus using local Ollama."""

import os
import subprocess
import sys
from typing import Any, Optional, TypedDict

import click
import httpx

# Maximum length for git diff to prevent overly long prompts
MAX_DIFF_LENGTH = 8000


class OllamaMessage(TypedDict):
    """Type for an Ollama API message."""

    role: str
    content: str


class OllamaRequest(TypedDict):
    """Type for an Ollama API request."""

    model: str
    messages: list[OllamaMessage]
    stream: bool
    options: dict[str, Any]


def get_git_diff() -> str:
    """Get the git diff of staged changes."""
    try:
        return subprocess.check_output(
            ["git", "diff", "--cached"], text=True, stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError:
        return ""


def get_git_status() -> str:
    """Get the git status of staged changes."""
    try:
        return subprocess.check_output(
            ["git", "status", "--porcelain"], text=True, stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError:
        return ""


def perform_git_commit(message: str) -> None:
    """Perform the git commit with the given message."""
    try:
        subprocess.run(["git", "commit", "-m", message], check=True, text=True)
        click.echo(f"Committed with message: {message}")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error committing: {e}", err=True)
        sys.exit(1)


def get_config_values() -> tuple[str, str, str]:
    """Get configuration values from config file or defaults.

    Returns:
        tuple: (ollama_host, model_name, prompt_message)
    """
    # Default values
    default_host = "http://localhost:11434"
    default_model = "llama3.2"
    default_prompt = (
        "You are an AI assistant that generates philosophical commit messages in the style of Albert Camus.\n"
        "Your task is to analyze git changes and create a commit message that reflects on the absurdity, rebellion, and human condition.\n\n"
        "Git Diff:\n{diff}\n\nGit Status:\n{status}\n\n"
        "Generate a philosophical commit message that:\n"
        "1. Reflects on the nature of the changes made\n"
        "2. Incorporates themes of existentialism and the absurd\n"
        "3. Is concise but meaningful (max 150 characters)\n"
        "4. Avoids technical jargon in favor of philosophical reflection\n\n"
        "Respond with only the commit message, no explanations or additional text."
    )

    try:
        from core.config import settings
        ollama_host = settings.ollama.host
        model_name = settings.run.model_name
        prompt_message = settings.run.prompt_message
    except Exception:
        ollama_host = default_host
        model_name = default_model
        prompt_message = default_prompt

    # Environment variables take precedence
    ollama_host = os.environ.get("OLLAMA_HOST", ollama_host)
    model_name = os.environ.get("OLLAMA_MODEL", model_name)

    return ollama_host, model_name, prompt_message


def generate_commit_message(diff: str, status: str) -> OllamaRequest:
    """Format the git diff and status data for the Ollama API.

    Args:
        diff: The git diff output
        status: The git status output

    Returns:
        OllamaRequest: The formatted request for the Ollama API
    """
    # Truncate diff if it's too long
    max_diff_length = MAX_DIFF_LENGTH
    if len(diff) > max_diff_length:
        diff = diff[:max_diff_length] + "\n... (truncated)"

    ollama_host, model_name, prompt_message = get_config_values()

    prompt = prompt_message.format(diff=diff, status=status)

    return {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0.7, "top_p": 0.9, "max_tokens": 150},
    }


def call_ollama_api(request_data: OllamaRequest) -> dict[str, Any]:
    """Call the local Ollama API to generate a commit message.

    Args:
        request_data: The formatted request data

    Returns:
        dict[str, Any]: The API response containing the generated message

    Raises:
        SystemExit: If the API call fails
    """
    ollama_host, _, _ = get_config_values()

    try:
        click.echo("Sending request to Ollama API...", err=True)
        response = httpx.post(f"{ollama_host}/api/chat", json=request_data, timeout=120.0)
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]
    except httpx.HTTPError as e:
        click.echo(f"API error: {e}", err=True)
        click.echo("Make sure Ollama is running and accessible", err=True)
        sys.exit(1)
    except httpx.ConnectError:
        click.echo(f"Could not connect to Ollama at {ollama_host}", err=True)
        click.echo("Make sure Ollama is running and the host/port is correct", err=True)
        sys.exit(1)


def run_git_camus(show: bool = False, message: Optional[str] = None) -> None:
    """Run the main git-camus logic.

    Args:
        show: If True, show the message without committing
        message: Optional context message to include in the prompt
    """
    # Check if we're in a git repository
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True
        )
    except subprocess.CalledProcessError:
        click.echo("Error: Not in a git repository", err=True)
        sys.exit(1)

    # Get git status and diff
    status = get_git_status()
    diff = get_git_diff()

    # Check if there are any staged changes
    if not status.strip():
        click.echo("No staged changes to commit.", err=True)
        sys.exit(0)

    # Generate the commit message
    request_data = generate_commit_message(diff, status)

    # Add context message if provided
    if message:
        context_prompt = f"Original commit message context: {message}\n\nPlease consider this context when generating the philosophical reflection."
        request_data["messages"].append({"role": "user", "content": context_prompt})

    # Call the API
    response = call_ollama_api(request_data)

    # Extract the commit message from the response
    commit_message = response.get("message", {}).get("content", "").strip()

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
def main(show: bool, message: Optional[str]) -> None:
    """Generate an existential commit message in the style of Albert Camus using local Ollama."""
    run_git_camus(show=show, message=message)


if __name__ == "__main__":
    main()

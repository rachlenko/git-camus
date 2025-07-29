#!/usr/bin/env python3
"""
Git-Camus: Craft Git Commit Messages with Existential Flair.

This tool transforms mundane git commit messages into philosophical reflections
inspired by the works of Albert Camus using a local Ollama service.
"""

import os
import subprocess
import sys
from typing import Dict, List, Optional, Union, TypedDict, Any

import click
import httpx


class OllamaMessage(TypedDict):
    """Type for an Ollama API message."""

    role: str
    content: str


class OllamaRequest(TypedDict):
    """Type for an Ollama API request."""

    model: str
    messages: List[OllamaMessage]
    stream: bool
    options: Dict[str, Any]


def get_git_diff() -> str:
    """Run `git diff --staged` to get the changes to be committed.

    Returns:
        str: The output of git diff showing pending changes.
    """
    try:
        return subprocess.check_output(["git", "diff", "--staged"], text=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error getting git diff: {e}", err=True)
        sys.exit(1)


def get_git_status() -> str:
    """Run `git status` to get the repository status.

    Returns:
        str: The output of git status.
    """
    try:
        return subprocess.check_output(["git", "status", "-s"], text=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error getting git status: {e}", err=True)
        sys.exit(1)


def generate_commit_message(diff: str, status: str) -> OllamaRequest:
    """Format the git diff and status data for the Ollama API.

    Args:
        diff: The output from git diff --staged
        status: The output from git status -s

    Returns:
        OllamaRequest: Request object for the Ollama API
    """
    # Truncate diff if it's too large to avoid excessive token usage
    max_diff_length = 4000
    if len(diff) > max_diff_length:
        diff = diff[:max_diff_length] + "\n... (truncated)"

    prompt = f"""You are an AI assistant that generates philosophical commit messages in the style of Albert Camus. 
Your task is to analyze git changes and create a commit message that reflects on the absurdity, rebellion, and human condition.

Git Status:
{status}

Git Diff:
{diff}

Generate a philosophical commit message inspired by Camus's existentialist philosophy. The message should:
1. Be concise (under 100 characters)
2. Reflect on the nature of the changes made
3. Incorporate themes of absurdity, rebellion, or the human condition
4. Be thoughtful and meaningful, not just a description

Respond with only the commit message, no additional text."""

    return {
        "model": os.environ.get("OLLAMA_MODEL", "llama3.2"),
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 150
        }
    }


def call_ollama_api(request_data: OllamaRequest) -> Dict[str, Any]:
    """Call the local Ollama API to generate a commit message.

    Args:
        request_data: Request data for the Ollama API

    Returns:
        Dict[str, Any]: The API response

    Raises:
        SystemExit: If the API call fails
    """
    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    
    try:
        # Debug information
        click.echo("Sending request to Ollama API...", err=True)

        response = httpx.post(
            f"{ollama_host}/api/chat",
            json=request_data,
            timeout=60.0,
        )

        # If we get an error, let's print more details
        if response.status_code != 200:
            click.echo(f"API error status: {response.status_code}", err=True)
            click.echo(f"Response body: {response.text}", err=True)
            click.echo(f"Make sure Ollama is running at {ollama_host}", err=True)

        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        click.echo(f"API error: {e}", err=True)
        click.echo("Make sure Ollama is running and accessible", err=True)
        sys.exit(1)
    except httpx.ConnectError:
        click.echo(f"Could not connect to Ollama at {ollama_host}", err=True)
        click.echo("Make sure Ollama is running and the host/port is correct", err=True)
        sys.exit(1)


def perform_git_commit(message: str) -> None:
    """Execute git commit with the provided message.

    Args:
        message: The commit message to use
    """
    try:
        subprocess.run(["git", "commit", "-m", message], check=True, text=True)
        click.echo(f"Committed with message: {message}")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error committing changes: {e}", err=True)
        sys.exit(1)


def run_git_camus(show: bool = False, message: Optional[str] = None) -> None:
    """Main logic for git-camus functionality.

    Args:
        show: If True, show the message without committing
        message: Optional original commit message to enhance
    """
    # Check if we're in a git repository
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError:
        click.echo("Error: Not in a git repository", err=True)
        sys.exit(1)

    # Get git status and diff
    status = get_git_status()
    diff = get_git_diff()

    if not status.strip() and not diff.strip():
        click.echo("No changes to commit", err=True)
        sys.exit(0)

    # Prepare API request
    request_data = generate_commit_message(diff, status)

    # Add original message context if provided
    if message:
        request_data["messages"].append(
            {"role": "user", "content": f"Consider this original message as context: {message}"}
        )

    # Call the API
    response = call_ollama_api(request_data)

    # Extract and process the commit message
    commit_message = response.get("message", {}).get("content", "").strip()

    if not commit_message:
        click.echo("Failed to generate a commit message", err=True)
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
    """Generate an existential commit message in the style of Albert Camus using local Ollama.

    If --show is specified, the message is displayed but not committed.
    If --message is provided, it will be used as context for generating the message.
    """
    run_git_camus(show=show, message=message)


if __name__ == "__main__":
    main()

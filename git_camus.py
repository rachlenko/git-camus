#!/usr/bin/env python3
"""
Git-Camus: Craft Git Commit Messages with Existential Flair.

This tool transforms mundane git commit messages into philosophical reflections
inspired by the works of Albert Camus.
"""

import os
import subprocess
import sys
from typing import Dict, List, Optional, Union, TypedDict, Any

import click
import httpx


class AnthropicMessage(TypedDict):
    """Type for a Claude API message."""

    role: str
    content: str


class AnthropicRequest(TypedDict):
    """Type for an Anthropic API request."""

    model: str
    max_tokens: int
    messages: List[AnthropicMessage]
    temperature: float


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


def generate_commit_message(diff: str, status: str) -> AnthropicRequest:
    """Format the git diff and status data for the Anthropic Claude API.

    Args:
        diff: The output from git diff --staged
        status: The output from git status -s

    Returns:
        AnthropicRequest: Request object for the Anthropic API
    """
    # Truncate diff if it's too large to avoid e


def call_anthropic_api(request_data: AnthropicRequest) -> Dict[str, Any]:
    """Call the Anthropic Claude API to generate a commit message.

    Args:
        request_data: Request data for the Anthropic API

    Returns:
        Dict[str, Any]: The API response

    Raises:
        SystemExit: If the API call fails
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        click.echo("Error: ANTHROPIC_API_KEY environment variable is not set", err=True)
        sys.exit(1)

    try:
        # Debug information
        click.echo("Sending request to Anthropic API...", err=True)

        response = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json=request_data,
            timeout=30.0,
        )

        # If we get an error, let's print more details
        if response.status_code != 200:
            click.echo(f"API error status: {response.status_code}", err=True)
            click.echo(f"Response body: {response.text}", err=True)

        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        click.echo(f"API error: {e}", err=True)
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


@click.command()
@click.option("--show", "-s", is_flag=True, help="Show the generated message without committing")
@click.option(
    "--message", "-m", help="Original commit message to enhance with Camus-style existentialism"
)
def main(show: bool, message: Optional[str]) -> None:
    """Generate an existential commit message in the style of Albert Camus.

    If --show is specified, the message is displayed but not committed.
    If --message is provided, it will be used as context for generating the message.
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
    response = call_anthropic_api(request_data)

    # Extract and process the commit message
    commit_message = response.get("content", [{}])[0].get("text", "").strip()

    if not commit_message:
        click.echo("Failed to generate a commit message", err=True)
        sys.exit(1)

    if show:
        click.echo(commit_message)
    else:
        perform_git_commit(commit_message)


if __name__ == "__main__":
    main()

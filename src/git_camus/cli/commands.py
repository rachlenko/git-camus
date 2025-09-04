"""CLI commands implementation."""

import sys
from typing import Optional

import click

from ..core.config import get_config_values
from ..core.git_operations import (
    check_git_repository,
    get_git_diff,
    get_git_status,
    has_staged_changes,
    perform_git_commit,
)
from ..core.ollama_client import OllamaClient


def run_git_camus(show: bool = False, message: Optional[str] = None) -> None:
    """Run the main git-camus logic.

    Args:
        show: If True, show the message without committing
        message: Optional context message to include in the prompt
    """
    # Check if we're in a git repository
    check_git_repository()

    # Get git status and diff
    status = get_git_status()
    diff = get_git_diff()

    # Check if there are any staged changes
    if not has_staged_changes(status):
        click.echo("No staged changes to commit.", err=True)
        sys.exit(0)

    # Get configuration
    ollama_host, model_name, prompt_message = get_config_values()
    
    # Initialize Ollama client
    client = OllamaClient(ollama_host)

    # Generate the commit message
    request_data = client.generate_commit_message_request(diff, status, model_name, prompt_message)

    # Add context message if provided
    if message:
        context_prompt = f"Original commit message context: {message}\n\nPlease consider this context when generating the philosophical reflection."
        request_data["messages"].append({"role": "user", "content": context_prompt})

    # Call the API
    response = client.call_api(request_data)

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
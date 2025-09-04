"""Git operations functionality."""

import subprocess
import sys
from typing import Optional

import click


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


def check_git_repository() -> None:
    """Check if we're in a git repository."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True
        )
    except subprocess.CalledProcessError:
        click.echo("Error: Not in a git repository", err=True)
        sys.exit(1)


def has_staged_changes(status: str) -> bool:
    """Check if there are any staged changes."""
    return bool(status.strip())
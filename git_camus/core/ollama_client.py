"""Ollama API client functionality."""

import sys
from typing import Any, TypedDict

import click
import httpx


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


class OllamaClient:
    """Client for interacting with Ollama API."""

    def __init__(self, host: str) -> None:
        """Initialize the Ollama client.
        
        Args:
            host: The Ollama host URL
        """
        self.host = host

    def generate_commit_message_request(
        self, diff: str, status: str, model_name: str, prompt_message: str, max_diff_length: int = 8000
    ) -> OllamaRequest:
        """Format the git diff and status data for the Ollama API.

        Args:
            diff: The git diff output
            status: The git status output
            model_name: The model to use
            prompt_message: The prompt template
            max_diff_length: Maximum length for git diff

        Returns:
            OllamaRequest: The formatted request for the Ollama API
        """
        # Truncate diff if it's too long
        if len(diff) > max_diff_length:
            diff = diff[:max_diff_length] + "\n... (truncated)"

        prompt = prompt_message.format(diff=diff, status=status)

        return {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": 0.7, "top_p": 0.9, "max_tokens": 150},
        }

    def call_api(self, request_data: OllamaRequest) -> dict[str, Any]:
        """Call the local Ollama API to generate a commit message.

        Args:
            request_data: The formatted request data

        Returns:
            dict[str, Any]: The API response containing the generated message

        Raises:
            SystemExit: If the API call fails
        """
        try:
            click.echo("Sending request to Ollama API...", err=True)
            response = httpx.post(f"{self.host}/api/chat", json=request_data, timeout=120.0)
            response.raise_for_status()
            return response.json()  # type: ignore[no-any-return]
        except httpx.HTTPError as e:
            click.echo(f"API error: {e}", err=True)
            click.echo("Make sure Ollama is running and accessible", err=True)
            sys.exit(1)
        except httpx.ConnectError:
            click.echo(f"Could not connect to Ollama at {self.host}", err=True)
            click.echo("Make sure Ollama is running and the host/port is correct", err=True)
            sys.exit(1)

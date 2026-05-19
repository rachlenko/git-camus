"""OpenAI API client functionality."""

import sys
from typing import Any

import click
import httpx


class OpenAIClient:
    """Client for interacting with OpenAI-compatible APIs."""

    def __init__(self, host: str, api_key: str) -> None:
        self.host = host
        self.api_key = api_key

    def generate_commit_message_request(
        self, diff: str, status: str, model_name: str, prompt_message: str, max_diff_length: int = 8000
    ) -> dict[str, Any]:
        if len(diff) > max_diff_length:
            diff = diff[:max_diff_length] + "\n... (truncated)"

        prompt = prompt_message.format(diff=diff, status=status)

        return {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 150,
        }

    def call_api(self, request_data: dict[str, Any]) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        try:
            click.echo("Sending request to OpenAI API...", err=True)
            response = httpx.post(
                f"{self.host}/chat/completions", json=request_data, headers=headers, timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            choices = data.get("choices", [])
            if not choices:
                return {"message": {"content": ""}}
            return {"message": choices[0].get("message", {})}
        except httpx.ConnectError:
            click.echo(f"Could not connect to OpenAI API at {self.host}", err=True)
            sys.exit(1)
        except httpx.HTTPError as e:
            click.echo(f"OpenAI API error: {e}", err=True)
            sys.exit(1)

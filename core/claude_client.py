"""Anthropic Claude API client functionality."""

import sys
from typing import Any

import click
import httpx

DEFAULT_SYSTEM_PROMPT = (
    "You are an AI assistant that generates philosophical commit messages in the style of Albert Camus. "
    "Your task is to analyze git changes and create a commit message that reflects on the absurdity, rebellion, and human condition."
)


class ClaudeClient:
    """Client for interacting with the Anthropic Messages API."""

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
            "max_tokens": 256,
            "system": DEFAULT_SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": prompt}],
        }

    def call_api(self, request_data: dict[str, Any]) -> dict[str, Any]:
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        try:
            click.echo("Sending request to Claude API...", err=True)
            response = httpx.post(
                f"{self.host}/v1/messages", json=request_data, headers=headers, timeout=120.0
            )
            response.raise_for_status()
            content_blocks = response.json().get("content", [])
            if not content_blocks:
                return {"message": {"content": ""}}
            return {"message": {"content": content_blocks[0].get("text", "")}}
        except httpx.ConnectError:
            click.echo(f"Could not connect to Claude API at {self.host}", err=True)
            sys.exit(1)
        except httpx.HTTPError as e:
            click.echo(f"Claude API error: {e}", err=True)
            sys.exit(1)

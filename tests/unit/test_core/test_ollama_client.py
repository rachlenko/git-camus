"""Tests for Ollama client module."""

from unittest.mock import Mock, patch

import httpx
import pytest

from git_camus.core.ollama_client import OllamaClient


class TestOllamaClient:
    """Test OllamaClient class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.host = "http://localhost:11434"
        self.client = OllamaClient(self.host)

    def test_init(self):
        """Test client initialization."""
        assert self.client.host == self.host

    def test_generate_commit_message_request(self):
        """Test commit message request generation."""
        diff = "diff --git a/file.txt b/file.txt\n+new line"
        status = "M  file.txt"
        model_name = "llama3.2"
        prompt_message = "Generate commit message for:\nDiff: {diff}\nStatus: {status}"
        
        request = self.client.generate_commit_message_request(
            diff, status, model_name, prompt_message
        )
        
        assert request["model"] == model_name
        assert request["stream"] is False
        assert len(request["messages"]) == 1
        assert request["messages"][0]["role"] == "user"
        assert "new line" in request["messages"][0]["content"]
        assert "M  file.txt" in request["messages"][0]["content"]
        assert request["options"]["temperature"] == 0.7

    def test_generate_commit_message_request_truncate_diff(self):
        """Test diff truncation for long diffs."""
        long_diff = "x" * 9000
        status = "M  file.txt"
        model_name = "llama3.2"
        prompt_message = "Diff: {diff}\nStatus: {status}"
        
        request = self.client.generate_commit_message_request(
            long_diff, status, model_name, prompt_message, max_diff_length=8000
        )
        
        content = request["messages"][0]["content"]
        assert "... (truncated)" in content
        assert len(content) < 9000

    @patch("httpx.post")
    def test_call_api_success(self, mock_post):
        """Test successful API call."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "message": {"content": "Philosophical commit message"}
        }
        mock_post.return_value = mock_response
        
        request_data = {
            "model": "llama3.2",
            "messages": [{"role": "user", "content": "test"}],
            "stream": False,
            "options": {}
        }
        
        result = self.client.call_api(request_data)
        
        assert result == {"message": {"content": "Philosophical commit message"}}
        mock_post.assert_called_once_with(
            f"{self.host}/api/chat", json=request_data, timeout=120.0
        )

    @patch("httpx.post")
    @patch("click.echo")
    def test_call_api_http_error(self, mock_echo, mock_post):
        """Test API call with HTTP error."""
        mock_post.side_effect = httpx.HTTPError("Connection failed")
        
        request_data = {"model": "test"}
        
        with pytest.raises(SystemExit):
            self.client.call_api(request_data)
        
        assert mock_echo.call_count == 2

    @patch("httpx.post")
    @patch("click.echo")
    def test_call_api_connection_error(self, mock_echo, mock_post):
        """Test API call with connection error."""
        mock_post.side_effect = httpx.ConnectError("Cannot connect")
        
        request_data = {"model": "test"}
        
        with pytest.raises(SystemExit):
            self.client.call_api(request_data)
        
        assert mock_echo.call_count == 2
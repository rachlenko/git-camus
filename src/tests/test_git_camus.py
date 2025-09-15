#!/usr/bin/env python3
"""Test suite for git-camus."""

import os
import subprocess
from unittest import mock

import httpx
import pytest

from git_camus.cli.commands import run_git_camus
from git_camus.core.git_operations import (
    get_git_diff,
    get_git_status,
    perform_git_commit,
)
from git_camus.core.ollama_client import OllamaClient


@pytest.fixture
def mock_ollama_env():
    """Mock Ollama environment variables."""
    with mock.patch.dict(
        os.environ, {"OLLAMA_HOST": "http://localhost:11434", "OLLAMA_MODEL": "llama3.2"}
    ):
        yield


@pytest.fixture
def mock_git_commands():
    """Mock all git subprocess commands."""
    with (
        mock.patch("subprocess.check_output") as mock_check_output,
        mock.patch("subprocess.run") as mock_run,
    ):
        # Set up git diff return value
        mock_check_output.side_effect = lambda cmd, **kwargs: {
            ("git", "diff", "--cached"): "diff --git a/test.py b/test.py\n+def test(): pass",
            ("git", "status", "--porcelain"): "M test.py",
        }.get(tuple(cmd), "")

        # Make subprocess.run return a successful result
        mock_run_result = mock.MagicMock()
        mock_run_result.returncode = 0
        mock_run.return_value = mock_run_result

        yield mock_check_output, mock_run


@pytest.fixture
def mock_ollama_api():
    """Mock Ollama API responses."""
    with mock.patch("httpx.post") as mock_post:
        # Create a mock response
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "message": {
                "content": "In the face of code's absurdity, we persist with new functions",
                "role": "assistant",
            }
        }
        mock_post.return_value = mock_response

        yield mock_post


class TestGitOperations:
    """Tests for Git operations."""

    def test_get_git_diff(self, mock_git_commands):
        """Test getting Git diff output."""
        mock_check_output, _ = mock_git_commands
        mock_check_output.return_value = (
            "diff --git a/test.py b/test.py\n+def new_function():\n    pass\n"
        )

        # Call the function
        result = get_git_diff()

        # Verify the result
        assert "diff --git" in result
        mock_check_output.assert_called_with(
            ["git", "diff", "--cached"], text=True, stderr=subprocess.PIPE
        )

    def test_get_git_diff_error(self):
        """Test error handling in get_git_diff."""
        with mock.patch("subprocess.check_output") as mock_check:
            mock_check.side_effect = subprocess.CalledProcessError(1, "git diff")

            # Call the function - should return empty string, not raise SystemExit
            result = get_git_diff()
            assert result == ""

    def test_get_git_status(self, mock_git_commands):
        """Test getting Git status output."""
        mock_check_output, _ = mock_git_commands
        mock_check_output.return_value = "M test.py"

        # Call the function
        result = get_git_status()

        # Verify the result
        assert "M test.py" in result
        mock_check_output.assert_called_with(
            ["git", "status", "--porcelain"], text=True, stderr=subprocess.PIPE
        )

    def test_get_git_status_error(self):
        """Test error handling in get_git_status."""
        with mock.patch("subprocess.check_output") as mock_check:
            mock_check.side_effect = subprocess.CalledProcessError(1, "git status")

            # Call the function - should return empty string, not raise SystemExit
            result = get_git_status()
            assert result == ""

    def test_perform_git_commit(self, mock_git_commands):
        """Test performing Git commit."""
        _, mock_run = mock_git_commands

        # Call the function
        perform_git_commit("Test commit message")

        # Verify the subprocess call
        mock_run.assert_called_with(
            ["git", "commit", "-m", "Test commit message"], check=True, text=True
        )

    def test_perform_git_commit_error(self):
        """Test error handling in perform_git_commit."""
        with mock.patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "git commit")

            with pytest.raises(SystemExit):
                perform_git_commit("Test commit message")


class TestAPIInteractions:
    """Tests for Ollama API interactions."""

    def test_generate_commit_message(self):
        """Test commit message request generation."""
        # Call the function
        client = OllamaClient(host="http://localhost:11434")
        request = client.generate_commit_message_request(
            "diff --git a/test.py b/test.py\n+def test(): pass", "M test.py"
        )

        # Verify the request structure
        assert isinstance(request, dict)
        assert "model" in request
        assert "messages" in request
        assert "stream" in request
        assert "options" in request
        assert len(request["messages"]) == 1
        assert request["messages"][0]["role"] == "user"
        assert "diff" in request["messages"][0]["content"]
        assert "Git Status:" in request["messages"][0]["content"]
        assert request["stream"] is False
        assert "temperature" in request["options"]
        assert "max_tokens" in request["options"]

    def test_call_ollama_api(self, mock_ollama_env, mock_ollama_api):
        """Test successful API call."""
        # Create test request data
        request_data = {
            "model": "llama3.2",
            "messages": [{"role": "user", "content": "Test message"}],
            "stream": False,
            "options": {"temperature": 0.7, "max_tokens": 150},
        }

        # Call the function
        client = OllamaClient(host="http://localhost:11434")
        response = client.call_api(request_data)

        # Verify API call
        mock_ollama_api.assert_called_once()
        args, kwargs = mock_ollama_api.call_args
        assert args[0] == "http://localhost:11434/api/chat"
        assert kwargs["json"] == request_data

        # Verify response processing
        assert "message" in response
        assert (
            response["message"]["content"]
            == "In the face of code's absurdity, we persist with new functions"
        )

    def test_call_ollama_api_connection_error(self, mock_ollama_env):
        """Test API call with connection error."""
        with mock.patch("httpx.post") as mock_post:
            mock_post.side_effect = httpx.ConnectError("Connection failed")

            with pytest.raises(SystemExit):
                client = OllamaClient(host="http://localhost:11434")
                client.call_api({})

    def test_call_ollama_api_http_error(self, mock_ollama_env):
        """Test API call with HTTP error."""
        with mock.patch("httpx.post") as mock_post:
            mock_post.side_effect = httpx.HTTPError("HTTP error")

            with pytest.raises(SystemExit):
                client = OllamaClient(host="http://localhost:11434")
                client.call_api({})

    def test_call_ollama_api_http_status_error(self, mock_ollama_env):
        """Test API call with HTTP status error."""
        with mock.patch("httpx.post") as mock_post:
            mock_response = mock.MagicMock()
            mock_response.status_code = 500
            mock_response.text = "Internal Server Error"
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "500 Internal Server Error", request=mock.MagicMock(), response=mock_response
            )
            mock_post.return_value = mock_response

            with pytest.raises(SystemExit):
                client = OllamaClient(host="http://localhost:11434")
                client.call_api({})

    def test_call_ollama_api_timeout_error(self, mock_ollama_env):
        """Test API call with timeout error."""
        with mock.patch("httpx.post") as mock_post:
            mock_post.side_effect = httpx.TimeoutException("Request timed out")

            with pytest.raises(SystemExit):
                client = OllamaClient(host="http://localhost:11434")
                client.call_api({})

    def test_generate_commit_message_with_large_diff(self):
        """Test commit message generation with large diff that gets truncated."""
        # Create a diff that's longer than MAX_DIFF_LENGTH (8000)
        large_diff = "diff --git a/test.py b/test.py\n" + "+" + "x" * 10000 + "\n"
        status = "M test.py"

        client = OllamaClient(host="http://localhost:11434")
        request = client.generate_commit_message_request(large_diff, status)

        # Verify the diff was truncated
        content = request["messages"][0]["content"]
        assert "... (truncated)" in content
        assert len(content) < 15000  # Should be much smaller than original

    def test_generate_commit_message_with_empty_diff(self):
        """Test commit message generation with empty diff."""
        request = generate_commit_message("", "M test.py")

        assert "Git Diff:" in request["messages"][0]["content"]
        assert request["model"] == "llama3.2"

    def test_generate_commit_message_with_custom_model(self):
        """Test commit message generation with custom model."""
        with mock.patch.dict(os.environ, {"OLLAMA_MODEL": "codellama"}):
            request = generate_commit_message("diff", "status")
            assert request["model"] == "codellama"

    def test_call_ollama_api_with_custom_host(self):
        """Test API call with custom host."""
        with mock.patch.dict(os.environ, {"OLLAMA_HOST": "http://custom-host:8080"}):
            with mock.patch("httpx.post") as mock_post:
                mock_response = mock.MagicMock()
                mock_response.status_code = 200
                mock_response.raise_for_status.return_value = None
                mock_response.json.return_value = {
                    "message": {"content": "Test response", "role": "assistant"}
                }
                mock_post.return_value = mock_response

                call_ollama_api(
                    {"model": "test", "messages": [], "stream": False, "options": {}}
                )

                # Verify custom host was used
                args, _ = mock_post.call_args
                assert args[0] == "http://custom-host:8080/api/chat"

    def test_perform_git_commit_success(self, mock_git_commands):
        """Test successful git commit."""
        _, mock_run = mock_git_commands

        with mock.patch("click.echo") as mock_echo:
            perform_git_commit("Test commit message")

            mock_run.assert_called_with(
                ["git", "commit", "-m", "Test commit message"], check=True, text=True
            )
            mock_echo.assert_called_with("Committed with message: Test commit message")

    def test_get_git_diff_with_stderr(self):
        """Test git diff with stderr output."""
        with mock.patch("subprocess.check_output") as mock_check:
            mock_check.return_value = "diff output"

            result = get_git_diff()
            assert result == "diff output"

    def test_get_git_status_with_stderr(self):
        """Test git status with stderr output."""
        with mock.patch("subprocess.check_output") as mock_check:
            mock_check.return_value = "status output"

            result = get_git_status()
            assert result == "status output"

    def test_run_git_camus_with_empty_response(self, mock_ollama_env, mock_git_commands):
        """Test run_git_camus with empty API response."""
        with mock.patch("httpx.post") as mock_post:
            mock_response = mock.MagicMock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"message": {"content": "", "role": "assistant"}}
            mock_post.return_value = mock_response

            with pytest.raises(SystemExit):
                run_git_camus(show=False, message=None)

    def test_run_git_camus_with_missing_message_key(self, mock_ollama_env, mock_git_commands):
        """Test run_git_camus with API response missing message key."""
        with mock.patch("httpx.post") as mock_post:
            mock_response = mock.MagicMock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"some_other_key": "value"}
            mock_post.return_value = mock_response

            with pytest.raises(SystemExit):
                run_git_camus(show=False, message=None)


class TestMainFunction:
    """Tests for main CLI function."""

    def test_run_git_camus_not_in_git_repo(self):
        """Test run_git_camus function outside of git repository."""
        with mock.patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(128, "git rev-parse")

            with pytest.raises(SystemExit):
                run_git_camus(show=False, message=None)

    def test_run_git_camus_no_changes(self, mock_git_commands):
        """Test run_git_camus function with no git changes."""
        mock_check_output, _ = mock_git_commands
        mock_check_output.side_effect = lambda cmd, **kwargs: ""

        with pytest.raises(SystemExit) as excinfo:
            git_camus.run_git_camus(show=False, message=None)

        assert excinfo.value.code == 0

    def test_run_git_camus_show_mode(self, mock_ollama_env, mock_git_commands, mock_ollama_api):
        """Test run_git_camus function in show mode (no commit)."""
        mock_check_output, _ = mock_git_commands
        # Mock the git commands to return proper values
        mock_check_output.side_effect = [
            "M test.py",  # git status
            "diff --git a/test.py b/test.py\n+def new_function():\n    pass\n",  # git diff
        ]

        with mock.patch("click.echo") as mock_echo:
            # Call the function in show mode
            run_git_camus(show=True, message=None)

            # Verify the output was shown
            mock_echo.assert_called_with(
                "In the face of code's absurdity, we persist with new functions"
            )

    def test_run_git_camus_with_message_context(
        self, mock_ollama_env, mock_git_commands, mock_ollama_api
    ):
        """Test run_git_camus function with message context."""
        mock_check_output, _ = mock_git_commands
        # Mock the git commands to return proper values
        mock_check_output.side_effect = [
            "M test.py",  # git status
            "diff --git a/test.py b/test.py\n+def new_function():\n    pass\n",  # git diff
        ]

        # Call the function with a message
        run_git_camus(show=False, message="Fix bug in authentication")

        # Verify the API request contained the context
        args, kwargs = mock_ollama_api.call_args
        messages = kwargs["json"]["messages"]
        assert len(messages) == 2
        assert "Fix bug in authentication" in messages[1]["content"]

    def test_run_git_camus_commit_mode(self, mock_ollama_env, mock_git_commands, mock_ollama_api):
        """Test run_git_camus function in commit mode."""
        mock_check_output, mock_run = mock_git_commands
        # Mock the git commands to return proper values
        mock_check_output.side_effect = [
            "M test.py",  # git status
            "diff --git a/test.py b/test.py\n+def new_function():\n    pass\n",  # git diff
        ]

        # Call the function in commit mode
        git_camus.run_git_camus(show=False, message=None)

        # Verify the commit was called
        commit_calls = [
            call
            for call in mock_run.call_args_list
            if call[0][0][0] == "git" and call[0][0][1] == "commit"
        ]
        assert len(commit_calls) == 1
        assert (
            commit_calls[0][0][0][3]
            == "In the face of code's absurdity, we persist with new functions"
        )

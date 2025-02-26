#!/usr/bin/env python3
"""Test suite for git-camus."""

import os
import subprocess
from unittest import mock

import httpx
import pytest

import git_camus


@pytest.fixture
def mock_api_key():
    """Mock API key environment variable."""
    with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-api-key"}):
        yield


@pytest.fixture
def mock_git_commands():
    """Mock all git subprocess commands."""
    with mock.patch("subprocess.check_output") as mock_check_output, \
         mock.patch("subprocess.run") as mock_run:
        # Set up git diff return value
        mock_check_output.side_effect = lambda cmd, **kwargs: {
            ('git', 'diff', '--staged'): "diff --git a/test.py b/test.py\n+def test(): pass",
            ('git', 'status', '-s'): "M test.py",
        }.get(tuple(cmd), "")
        
        # Make subprocess.run return a successful result
        mock_run_result = mock.MagicMock()
        mock_run_result.returncode = 0
        mock_run.return_value = mock_run_result
        
        yield mock_check_output, mock_run


@pytest.fixture
def mock_anthropic_api():
    """Mock Anthropic API responses."""
    with mock.patch("httpx.post") as mock_post:
        # Create a mock response
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "content": [{"text": "Confront the absurd: Add test function", "type": "text"}]
        }
        mock_post.return_value = mock_response
        
        yield mock_post


class TestGitOperations:
    """Tests for Git operations."""
    
    def test_get_git_diff(self, mock_git_commands):
        """Test getting Git diff output."""
        mock_check_output, _ = mock_git_commands
        
        # Call the function
        result = git_camus.get_git_diff()
        
        # Verify the result
        assert "diff --git" in result
        mock_check_output.assert_called_with(["git", "diff", "--staged"], text=True)
    
    def test_get_git_diff_error(self):
        """Test error handling in get_git_diff."""
        with mock.patch("subprocess.check_output") as mock_check:
            mock_check.side_effect = subprocess.CalledProcessError(1, "git diff")
            
            with pytest.raises(SystemExit):
                git_camus.get_git_diff()
    
    def test_get_git_status(self, mock_git_commands):
        """Test getting Git status output."""
        mock_check_output, _ = mock_git_commands
        
        # Call the function
        result = git_camus.get_git_status()
        
        # Verify the result
        assert "M test.py" in result
        mock_check_output.assert_called_with(["git", "status", "-s"], text=True)
    
    def test_get_git_status_error(self):
        """Test error handling in get_git_status."""
        with mock.patch("subprocess.check_output") as mock_check:
            mock_check.side_effect = subprocess.CalledProcessError(1, "git status")
            
            with pytest.raises(SystemExit):
                git_camus.get_git_status()
    
    def test_perform_git_commit(self, mock_git_commands):
        """Test performing Git commit."""
        _, mock_run = mock_git_commands
        
        # Call the function
        git_camus.perform_git_commit("Test commit message")
        
        # Verify the subprocess call
        mock_run.assert_called_with(
            ["git", "commit", "-m", "Test commit message"],
            check=True,
            text=True
        )
    
    def test_perform_git_commit_error(self):
        """Test error handling in perform_git_commit."""
        with mock.patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "git commit")
            
            with pytest.raises(SystemExit):
                git_camus.perform_git_commit("Test commit message")


class TestAPIInteractions:
    """Tests for Anthropic API interactions."""
    
    def test_generate_commit_message(self):
        """Test commit message request generation."""
        # Call the function
        request = git_camus.generate_commit_message(
            "diff --git a/test.py b/test.py\n+def test(): pass",
            "M test.py"
        )
        
        # Verify the request structure
        assert isinstance(request, dict)
        assert "model" in request
        assert "messages" in request
        assert len(request["messages"]) == 2
        assert request["messages"][0]["role"] == "system"
        assert request["messages"][1]["role"] == "user"
        assert "diff" in request["messages"][1]["content"]
        assert "status" in request["messages"][1]["content"]
    
    def test_call_anthropic_api(self, mock_api_key, mock_anthropic_api):
        """Test successful API call."""
        # Create test request data
        request_data = {
            "model": "claude-3-5-sonnet-20240620",
            "messages": [{"role": "user", "content": "Test message"}],
            "max_tokens": 150
        }
        
        # Call the function
        response = git_camus.call_anthropic_api(request_data)
        
        # Verify API call
        mock_anthropic_api.assert_called_once()
        args, kwargs = mock_anthropic_api.call_args
        assert args[0] == "https://api.anthropic.com/v1/messages"
        assert kwargs["headers"]["x-api-key"] == "test-api-key"
        assert kwargs["json"] == request_data
        
        # Verify response processing
        assert "content" in response
        assert response["content"][0]["text"] == "Confront the absurd: Add test function"
    
    def test_call_anthropic_api_no_key(self):
        """Test API call without API key."""
        with mock.patch.dict(os.environ, {}, clear=True):
            with pytest.raises(SystemExit):
                git_camus.call_anthropic_api({})
    
    def test_call_anthropic_api_error(self, mock_api_key):
        """Test API call with error response."""
        with mock.patch("httpx.post") as mock_post:
            mock_post.side_effect = httpx.HTTPError("API error")
            
            with pytest.raises(SystemExit):
                git_camus.call_anthropic_api({})


class TestMainFunction:
    """Tests for main CLI function."""
    
    def test_main_not_in_git_repo(self):
        """Test main function outside of git repository."""
        with mock.patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(128, "git rev-parse")
            
            with pytest.raises(SystemExit):
                git_camus.main(show=False, message=None)
    
    def test_main_no_changes(self, mock_git_commands):
        """Test main function with no git changes."""
        mock_check_output, _ = mock_git_commands
        mock_check_output.side_effect = lambda cmd, **kwargs: "" 
        
        with pytest.raises(SystemExit) as excinfo:
            git_camus.main(show=False, message=None)
        
        assert excinfo.value.code == 0
    
    def test_main_show_mode(self, mock_api_key, mock_git_commands, mock_anthropic_api):
        """Test main function in show mode (no commit)."""
        with mock.patch("click.echo") as mock_echo:
            # Call the function in show mode
            git_camus.main(show=True, message=None)
            
            # Verify echo was called with the commit message
            mock_echo.assert_called_with("Confront the absurd: Add test function")
            
            # Make sure git commit was not called
            _, mock_run = mock_git_commands
            for call in mock_run.call_args_list:
                assert not (call[0][0][0] == "git" and call[0][0][1] == "commit")
    
    def test_main_with_message_context(self, mock_api_key, mock_git_commands, mock_anthropic_api):
        """Test main function with message context."""
        # Call the function with a message
        git_camus.main(show=False, message="Fix bug in authentication")
        
        # Verify the API request contained the original message
        args, kwargs = mock_anthropic_api.call_args
        messages = kwargs["json"]["messages"]
        assert len(messages) == 3
        assert "Fix bug in authentication" in messages[2]["content"]
    
    def test_main_commit_mode(self, mock_api_key, mock_git_commands, mock_anthropic_api):
        """Test main function in commit mode."""
        # Call the function in commit mode
        git_camus.main(show=False, message=None)
        
        # Check that git commit was called with the generated message
        _, mock_run = mock_git_commands
        commit_calls = [call for call in mock_run.call_args_list if 
                        call[0][0][0] == "git" and call[0][0][1] == "commit"]
        assert len(commit_calls) == 1
        assert commit_calls[0][0][0][3] == "Confront the absurd: Add test function"
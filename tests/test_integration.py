#!/usr/bin/env python3
"""Integration tests for git-camus with Ollama."""

import os
import subprocess
import tempfile
from pathlib import Path
from unittest import mock

import httpx
import pytest

from git_camus.cli.commands import run_git_camus


class TestGitCamusIntegration:
    """Integration tests for the complete git-camus workflow."""

    @pytest.fixture
    def temp_git_repo(self):
        """Create a temporary git repository for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)

            # Initialize git repository
            subprocess.run(["git", "init"], cwd=repo_path, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"], cwd=repo_path, check=True
            )

            # Create initial commit
            (repo_path / "README.md").write_text("# Test Project\n")
            subprocess.run(["git", "add", "README.md"], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path, check=True)

            yield repo_path

    @pytest.fixture
    def mock_ollama_env(self):
        """Mock Ollama environment variables."""
        with mock.patch.dict(
            os.environ, {"OLLAMA_HOST": "http://localhost:11434", "OLLAMA_MODEL": "llama3.2"}
        ):
            yield

    @pytest.fixture
    def mock_ollama_api(self):
        """Mock Ollama API responses."""
        with mock.patch("httpx.post") as mock_post:
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

    def test_complete_workflow_show_mode(self, temp_git_repo, mock_ollama_env, mock_ollama_api):
        """Test complete workflow in show mode."""
        # Create a test file
        test_file = temp_git_repo / "test.py"
        test_file.write_text("def new_function():\n    pass\n")

        # Stage the changes
        subprocess.run(["git", "add", "test.py"], cwd=temp_git_repo, check=True)

        # Mock click.echo to capture output
        with mock.patch("click.echo") as mock_echo:
            # Change to the temp directory and run git-camus
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_git_repo)
                run_git_camus(show=True, message=None)

                # Verify the output
                mock_echo.assert_called_with(
                    "In the face of code's absurdity, we persist with new functions"
                )

                # Verify no commit was made
                result = subprocess.run(
                    ["git", "log", "--oneline"],
                    cwd=temp_git_repo,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                assert result.stdout.count("\n") == 1  # Only initial commit

            finally:
                os.chdir(original_cwd)

    def test_complete_workflow_commit_mode(self, temp_git_repo, mock_ollama_env, mock_ollama_api):
        """Test complete workflow in commit mode."""
        # Create a test file
        test_file = temp_git_repo / "test.py"
        test_file.write_text("def new_function():\n    pass\n")

        # Stage the changes
        subprocess.run(["git", "add", "test.py"], cwd=temp_git_repo, check=True)

        # Change to the temp directory and run git-camus
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_git_repo)
            run_git_camus(show=False, message=None)

            # Verify commit was made
            result = subprocess.run(
                ["git", "log", "--oneline"],
                cwd=temp_git_repo,
                capture_output=True,
                text=True,
                check=True,
            )
            assert result.stdout.count("\n") == 2  # Initial commit + new commit

            # Verify commit message
            result = subprocess.run(
                ["git", "log", "-1", "--pretty=format:%s"],
                cwd=temp_git_repo,
                capture_output=True,
                text=True,
                check=True,
            )
            assert "In the face of code's absurdity" in result.stdout

        finally:
            os.chdir(original_cwd)

    def test_workflow_with_message_context(self, temp_git_repo, mock_ollama_env, mock_ollama_api):
        """Test workflow with custom message context."""
        # Create a test file
        test_file = temp_git_repo / "test.py"
        test_file.write_text("def new_function():\n    pass\n")

        # Stage the changes
        subprocess.run(["git", "add", "test.py"], cwd=temp_git_repo, check=True)

        # Change to the temp directory and run git-camus
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_git_repo)
            run_git_camus(show=False, message="Add new function")

            # Verify the API request contained the context
            args, kwargs = mock_ollama_api.call_args
            messages = kwargs["json"]["messages"]
            assert len(messages) == 2
            assert "Add new function" in messages[1]["content"]

        finally:
            os.chdir(original_cwd)

    def test_workflow_with_large_diff(self, temp_git_repo, mock_ollama_env, mock_ollama_api):
        """Test workflow with a large diff that should be truncated."""
        # Create a large test file
        test_file = temp_git_repo / "large_test.py"
        large_content = "def large_function():\n" + "    " + "pass\n" * 2000  # Very large file
        test_file.write_text(large_content)

        # Stage the changes
        subprocess.run(["git", "add", "large_test.py"], cwd=temp_git_repo, check=True)

        # Change to the temp directory and run git-camus
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_git_repo)
            git_camus.run_git_camus(show=True, message=None)

            # Verify the API request was made (diff should be truncated)
            args, kwargs = mock_ollama_api.call_args
            content = kwargs["json"]["messages"][0]["content"]
            assert "truncated" in content

        finally:
            os.chdir(original_cwd)

    def test_workflow_no_changes(self, temp_git_repo, mock_ollama_env):
        """Test workflow when there are no changes to commit."""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_git_repo)

            with pytest.raises(SystemExit) as excinfo:
                run_git_camus(show=False, message=None)

            assert excinfo.value.code == 0

        finally:
            os.chdir(original_cwd)

    def test_workflow_not_in_git_repo(self, mock_ollama_env):
        """Test workflow when not in a git repository."""
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)

                with pytest.raises(SystemExit):
                    run_git_camus(show=False, message=None)

            finally:
                os.chdir(original_cwd)

    def test_workflow_ollama_connection_error(self, temp_git_repo, mock_ollama_env):
        """Test workflow when Ollama is not available."""
        # Create a test file
        test_file = temp_git_repo / "test.py"
        test_file.write_text("def new_function():\n    pass\n")

        # Stage the changes
        subprocess.run(["git", "add", "test.py"], cwd=temp_git_repo, check=True)

        # Mock connection error
        with mock.patch("httpx.post") as mock_post:
            mock_post.side_effect = httpx.ConnectError("Connection failed")

            original_cwd = os.getcwd()
            try:
                os.chdir(temp_git_repo)

                with pytest.raises(SystemExit):
                    run_git_camus(show=False, message=None)

            finally:
                os.chdir(original_cwd)

    def test_workflow_custom_ollama_host(self, temp_git_repo, mock_ollama_api):
        """Test workflow with custom Ollama host."""
        # Create a test file
        test_file = temp_git_repo / "test.py"
        test_file.write_text("def new_function():\n    pass\n")

        # Stage the changes
        subprocess.run(["git", "add", "test.py"], cwd=temp_git_repo, check=True)

        # Set custom Ollama host
        with mock.patch.dict(
            os.environ, {"OLLAMA_HOST": "http://custom-host:8080", "OLLAMA_MODEL": "llama3.2"}
        ):
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_git_repo)
                run_git_camus(show=True, message=None)

                # Verify custom host was used
                args, _ = mock_ollama_api.call_args
                assert args[0] == "http://custom-host:8080/api/chat"

            finally:
                os.chdir(original_cwd)

    def test_workflow_custom_model(self, temp_git_repo, mock_ollama_api):
        """Test workflow with custom Ollama model."""
        # Create a test file
        test_file = temp_git_repo / "test.py"
        test_file.write_text("def new_function():\n    pass\n")

        # Stage the changes
        subprocess.run(["git", "add", "test.py"], cwd=temp_git_repo, check=True)

        # Set custom model
        with mock.patch.dict(
            os.environ, {"OLLAMA_HOST": "http://localhost:11434", "OLLAMA_MODEL": "codellama"}
        ):
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_git_repo)
                run_git_camus(show=True, message=None)

                # Verify custom model was used
                args, kwargs = mock_ollama_api.call_args
                assert kwargs["json"]["model"] == "codellama"

            finally:
                os.chdir(original_cwd)

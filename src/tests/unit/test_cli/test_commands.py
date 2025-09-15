"""Tests for CLI commands module."""

from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from git_camus.cli.commands import main, run_git_camus


class TestRunGitCamus:
    """Test run_git_camus function."""

    @patch("git_camus.cli.commands.check_git_repository")
    @patch("git_camus.cli.commands.get_git_status")
    @patch("git_camus.cli.commands.get_git_diff")
    @patch("git_camus.cli.commands.has_staged_changes")
    @patch("git_camus.cli.commands.get_config_values")
    @patch("git_camus.cli.commands.OllamaClient")
    @patch("git_camus.cli.commands.perform_git_commit")
    def test_run_git_camus_commit_success(
        self,
        mock_commit,
        mock_ollama_client,
        mock_config,
        mock_has_changes,
        mock_diff,
        mock_status,
        mock_check_repo
    ):
        """Test successful commit flow."""
        # Setup mocks
        mock_status.return_value = "M  file.txt"
        mock_diff.return_value = "diff content"
        mock_has_changes.return_value = True
        mock_config.return_value = ("http://localhost:11434", "llama3.2", "prompt")

        mock_client_instance = Mock()
        mock_ollama_client.return_value = mock_client_instance
        mock_client_instance.generate_commit_message_request.return_value = {"messages": []}
        mock_client_instance.call_api.return_value = {
            "message": {"content": "Philosophical commit message"}
        }

        # Run function
        run_git_camus(show=False, message=None)

        # Verify calls
        mock_check_repo.assert_called_once()
        mock_commit.assert_called_once_with("Philosophical commit message")

    @patch("git_camus.cli.commands.check_git_repository")
    @patch("git_camus.cli.commands.get_git_status")
    @patch("git_camus.cli.commands.has_staged_changes")
    @patch("click.echo")
    def test_run_git_camus_no_staged_changes(
        self,
        mock_echo,
        mock_has_changes,
        mock_status,
        mock_check_repo
    ):
        """Test behavior when no staged changes."""
        mock_status.return_value = ""
        mock_has_changes.return_value = False

        with pytest.raises(SystemExit):
            run_git_camus()

        mock_echo.assert_called_once_with("No staged changes to commit.", err=True)

    @patch("git_camus.cli.commands.check_git_repository")
    @patch("git_camus.cli.commands.get_git_status")
    @patch("git_camus.cli.commands.get_git_diff")
    @patch("git_camus.cli.commands.has_staged_changes")
    @patch("git_camus.cli.commands.get_config_values")
    @patch("git_camus.cli.commands.OllamaClient")
    @patch("click.echo")
    def test_run_git_camus_show_message(
        self,
        mock_echo,
        mock_ollama_client,
        mock_config,
        mock_has_changes,
        mock_diff,
        mock_status,
        mock_check_repo
    ):
        """Test show message without committing."""
        # Setup mocks
        mock_status.return_value = "M  file.txt"
        mock_diff.return_value = "diff content"
        mock_has_changes.return_value = True
        mock_config.return_value = ("http://localhost:11434", "llama3.2", "prompt")

        mock_client_instance = Mock()
        mock_ollama_client.return_value = mock_client_instance
        mock_client_instance.generate_commit_message_request.return_value = {"messages": []}
        mock_client_instance.call_api.return_value = {
            "message": {"content": "Philosophical commit message"}
        }

        # Run function with show=True
        run_git_camus(show=True, message=None)

        # Verify message is displayed, not committed
        mock_echo.assert_called_once_with("Philosophical commit message")

    @patch("git_camus.cli.commands.check_git_repository")
    @patch("git_camus.cli.commands.get_git_status")
    @patch("git_camus.cli.commands.get_git_diff")
    @patch("git_camus.cli.commands.has_staged_changes")
    @patch("git_camus.cli.commands.get_config_values")
    @patch("git_camus.cli.commands.OllamaClient")
    @patch("click.echo")
    def test_run_git_camus_empty_response(
        self,
        mock_echo,
        mock_ollama_client,
        mock_config,
        mock_has_changes,
        mock_diff,
        mock_status,
        mock_check_repo
    ):
        """Test behavior when API returns empty response."""
        # Setup mocks
        mock_status.return_value = "M  file.txt"
        mock_diff.return_value = "diff content"
        mock_has_changes.return_value = True
        mock_config.return_value = ("http://localhost:11434", "llama3.2", "prompt")

        mock_client_instance = Mock()
        mock_ollama_client.return_value = mock_client_instance
        mock_client_instance.generate_commit_message_request.return_value = {"messages": []}
        mock_client_instance.call_api.return_value = {"message": {"content": ""}}

        with pytest.raises(SystemExit):
            run_git_camus()

        mock_echo.assert_called_once_with("Error: No commit message generated", err=True)


class TestCliCommands:
    """Test CLI command interface."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch("git_camus.cli.commands.run_git_camus")
    def test_main_command_default(self, mock_run):
        """Test main command with default options."""
        result = self.runner.invoke(main, [])

        assert result.exit_code == 0
        mock_run.assert_called_once_with(show=False, message=None)

    @patch("git_camus.cli.commands.run_git_camus")
    def test_main_command_with_show(self, mock_run):
        """Test main command with show flag."""
        result = self.runner.invoke(main, ["--show"])

        assert result.exit_code == 0
        mock_run.assert_called_once_with(show=True, message=None)

    @patch("git_camus.cli.commands.run_git_camus")
    def test_main_command_with_message(self, mock_run):
        """Test main command with message option."""
        result = self.runner.invoke(main, ["--message", "test message"])

        assert result.exit_code == 0
        mock_run.assert_called_once_with(show=False, message="test message")

    @patch("git_camus.cli.commands.run_git_camus")
    def test_main_command_with_both_options(self, mock_run):
        """Test main command with both options."""
        result = self.runner.invoke(main, ["-s", "-m", "test message"])

        assert result.exit_code == 0
        mock_run.assert_called_once_with(show=True, message="test message")

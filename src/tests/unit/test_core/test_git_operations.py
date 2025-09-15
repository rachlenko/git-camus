"""Tests for git operations module."""

import subprocess
from unittest.mock import patch

import pytest

from git_camus.core.git_operations import (
    check_git_repository,
    get_git_diff,
    get_git_status,
    has_staged_changes,
    perform_git_commit,
)


class TestGetGitDiff:
    """Test get_git_diff function."""

    @patch("subprocess.check_output")
    def test_get_git_diff_success(self, mock_check_output):
        """Test successful git diff retrieval."""
        expected_diff = "diff --git a/file.txt b/file.txt\n+new line"
        mock_check_output.return_value = expected_diff

        result = get_git_diff()

        assert result == expected_diff
        mock_check_output.assert_called_once_with(
            ["git", "diff", "--cached"], text=True, stderr=subprocess.PIPE
        )

    @patch("subprocess.check_output")
    def test_get_git_diff_failure(self, mock_check_output):
        """Test git diff failure returns empty string."""
        mock_check_output.side_effect = subprocess.CalledProcessError(1, "git")

        result = get_git_diff()

        assert result == ""


class TestGetGitStatus:
    """Test get_git_status function."""

    @patch("subprocess.check_output")
    def test_get_git_status_success(self, mock_check_output):
        """Test successful git status retrieval."""
        expected_status = "M  file.txt\nA  new_file.txt"
        mock_check_output.return_value = expected_status

        result = get_git_status()

        assert result == expected_status
        mock_check_output.assert_called_once_with(
            ["git", "status", "--porcelain"], text=True, stderr=subprocess.PIPE
        )

    @patch("subprocess.check_output")
    def test_get_git_status_failure(self, mock_check_output):
        """Test git status failure returns empty string."""
        mock_check_output.side_effect = subprocess.CalledProcessError(1, "git")

        result = get_git_status()

        assert result == ""


class TestPerformGitCommit:
    """Test perform_git_commit function."""

    @patch("subprocess.run")
    @patch("click.echo")
    def test_perform_git_commit_success(self, mock_echo, mock_run):
        """Test successful git commit."""
        message = "Test commit message"

        perform_git_commit(message)

        mock_run.assert_called_once_with(
            ["git", "commit", "-m", message], check=True, text=True
        )
        mock_echo.assert_called_once_with(f"Committed with message: {message}")

    @patch("subprocess.run")
    @patch("click.echo")
    def test_perform_git_commit_failure(self, mock_echo, mock_run):
        """Test git commit failure exits with error."""
        message = "Test commit message"
        error = subprocess.CalledProcessError(1, "git")
        mock_run.side_effect = error

        with pytest.raises(SystemExit):
            perform_git_commit(message)

        mock_echo.assert_called_once_with(f"Error committing: {error}", err=True)


class TestCheckGitRepository:
    """Test check_git_repository function."""

    @patch("subprocess.run")
    def test_check_git_repository_success(self, mock_run):
        """Test successful git repository check."""
        check_git_repository()

        mock_run.assert_called_once_with(
            ["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True
        )

    @patch("subprocess.run")
    @patch("click.echo")
    def test_check_git_repository_failure(self, mock_echo, mock_run):
        """Test git repository check failure exits with error."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git")

        with pytest.raises(SystemExit):
            check_git_repository()

        mock_echo.assert_called_once_with("Error: Not in a git repository", err=True)


class TestHasStagedChanges:
    """Test has_staged_changes function."""

    def test_has_staged_changes_true(self):
        """Test returns True for non-empty status."""
        status = "M  file.txt\nA  new_file.txt"
        assert has_staged_changes(status) is True

    def test_has_staged_changes_false_empty(self):
        """Test returns False for empty status."""
        status = ""
        assert has_staged_changes(status) is False

    def test_has_staged_changes_false_whitespace(self):
        """Test returns False for whitespace-only status."""
        status = "   \n  \t  "
        assert has_staged_changes(status) is False

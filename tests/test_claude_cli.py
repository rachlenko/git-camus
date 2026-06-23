#!/usr/bin/env python3
"""Tests for the claude-cli provider (uses `claude -p`, no API key)."""

import subprocess

import pytest

import git_camus


def test_claude_cli_in_providers():
    assert "claude-cli" in git_camus.PROVIDERS


def test_get_config_values_claude_cli_needs_no_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    host, model, prompt, api_key = git_camus.get_config_values("claude-cli")
    assert api_key is None
    assert isinstance(prompt, str) and prompt


def test_call_claude_cli_success_strips_api_key(monkeypatch):
    captured = {}

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        captured["env"] = kwargs.get("env")
        return subprocess.CompletedProcess(cmd, 0, stdout="A rebellion of bytes\n", stderr="")

    monkeypatch.setenv("ANTHROPIC_API_KEY", "op://bad")
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "tok")
    monkeypatch.setattr(subprocess, "run", fake_run)

    msg = git_camus.call_claude_cli([{"role": "user", "content": "Git Diff: x"}])

    assert msg == "A rebellion of bytes"
    assert captured["cmd"][:2] == ["claude", "-p"]
    # The CLI must run without the (invalid) API key so it uses its own login.
    assert "ANTHROPIC_API_KEY" not in captured["env"]
    assert "ANTHROPIC_AUTH_TOKEN" not in captured["env"]


def test_call_claude_cli_binary_not_found(monkeypatch):
    def fake_run(cmd, **kwargs):
        raise FileNotFoundError(cmd[0])

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(SystemExit):
        git_camus.call_claude_cli([{"role": "user", "content": "x"}])


def test_call_claude_cli_nonzero_exit(monkeypatch):
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 1, stdout="", stderr="boom")

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(SystemExit):
        git_camus.call_claude_cli([{"role": "user", "content": "x"}])


def test_run_git_camus_routes_to_claude_cli(monkeypatch, capsys):
    monkeypatch.setattr(git_camus, "get_git_status", lambda: " M file.py\n")
    monkeypatch.setattr(git_camus, "get_git_diff", lambda: "diff")

    def fake_run(cmd, **kwargs):
        # git rev-parse --is-inside-work-tree
        if cmd[:2] == ["git", "rev-parse"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="true\n", stderr="")
        # claude -p ...
        return subprocess.CompletedProcess(cmd, 0, stdout="Existence precedes commit\n", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    git_camus.run_git_camus(show=True, message=None, provider="claude-cli")
    out = capsys.readouterr().out
    assert "Existence precedes commit" in out


def test_call_claude_cli_strips_code_fences(monkeypatch):
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 0, stdout="```\nfeat: rebel against entropy\n```\n", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert git_camus.call_claude_cli([{"role": "user", "content": "x"}]) == "feat: rebel against entropy"


def test_call_claude_cli_strips_language_fence(monkeypatch):
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 0, stdout="```text\nfix: the absurd\n```", stderr="")
    monkeypatch.setattr(subprocess, "run", fake_run)
    assert git_camus.call_claude_cli([{"role": "user", "content": "x"}]) == "fix: the absurd"


def test_call_claude_cli_plain_text_unchanged(monkeypatch):
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 0, stdout="docs: a plain line\n", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert git_camus.call_claude_cli([{"role": "user", "content": "x"}]) == "docs: a plain line"

"""Tests for configuration module."""

import os
from unittest.mock import patch

from git_camus.core.config import get_config_values, settings


class TestGetConfigValues:
    """Test get_config_values function."""

    def test_get_config_values_defaults(self):
        """Test getting default configuration values."""
        with patch.dict(os.environ, {}, clear=True):
            host, model, prompt = get_config_values()

            assert host == "http://localhost:11434"
            assert model == "llama3.2"
            assert "Albert Camus" in prompt

    def test_get_config_values_with_env_vars(self):
        """Test configuration with environment variables."""
        test_env = {
            "OLLAMA_HOST": "http://test:8080",
            "OLLAMA_MODEL": "test-model"
        }

        with patch.dict(os.environ, test_env, clear=True):
            host, model, prompt = get_config_values()

            assert host == "http://test:8080"
            assert model == "test-model"
            assert "Albert Camus" in prompt

    def test_get_config_values_with_settings(self):
        """Test configuration with settings override."""
        with patch.object(settings, "ollama") as mock_ollama, \
             patch.object(settings, "run") as mock_run:

            mock_ollama.host = "http://settings:9999"
            mock_run.model_name = "settings-model"
            mock_run.prompt_message = "Settings prompt"

            with patch.dict(os.environ, {}, clear=True):
                host, model, prompt = get_config_values()

                assert host == "http://settings:9999"
                assert model == "settings-model"
                assert prompt == "Settings prompt"

    def test_get_config_values_env_overrides_settings(self):
        """Test environment variables override settings."""
        with patch.object(settings, "ollama") as mock_ollama, \
             patch.object(settings, "run") as mock_run:

            mock_ollama.host = "http://settings:9999"
            mock_run.model_name = "settings-model"

            test_env = {
                "OLLAMA_HOST": "http://env:7777",
                "OLLAMA_MODEL": "env-model"
            }

            with patch.dict(os.environ, test_env, clear=True):
                host, model, prompt = get_config_values()

                assert host == "http://env:7777"
                assert model == "env-model"

    def test_get_config_values_exception_fallback(self):
        """Test fallback to defaults when settings raise exception."""
        with patch.object(settings, "ollama", side_effect=Exception("Test error")):
            with patch.dict(os.environ, {}, clear=True):
                host, model, prompt = get_config_values()

                assert host == "http://localhost:11434"
                assert model == "llama3.2"
                assert "Albert Camus" in prompt


class TestSettings:
    """Test settings configuration."""

    def test_settings_default_values(self):
        """Test default settings values."""
        assert settings.ollama.host == "http://localhost:11434"
        assert settings.run.model_name == "llama3.2"
        assert "Albert Camus" in settings.run.prompt_message
        assert settings.api.prefix == "/api"

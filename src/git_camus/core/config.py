"""Configuration management for git-camus."""

import os
from typing import Tuple

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class OllamaConfig(BaseModel):
    """Ollama API configuration."""
    host: str = "http://localhost:11434"


class RunConfig(BaseModel):
    """Runtime configuration."""
    host: str = "0.0.0.0"
    port: int = 8000
    model_name: str = "llama3.2"  # Default model name for Ollama
    prompt_message: str = (
        "You are an AI assistant that generates philosophical commit messages in the style of Albert Camus.\n"
        "Your task is to analyze git changes and create a commit message that reflects on the absurdity, rebellion, and human condition.\n\n"
        "Git Diff:\n{diff}\n\nGit Status:\n{status}\n\n"
        "Generate a philosophical commit message that:\n"
        "1. Reflects on the nature of the changes made\n"
        "2. Incorporates themes of existentialism and the absurd\n"
        "3. Is concise but meaningful (max 150 characters)\n"
        "4. Avoids technical jargon in favor of philosophical reflection\n\n"
        "Respond with only the commit message, no explanations or additional text."
    )


class ApiPrefix(BaseModel):
    """API prefix configuration."""
    prefix: str = "/api"


class Settings(BaseSettings):
    """Application settings."""
    ollama: OllamaConfig = OllamaConfig()
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()


settings = Settings()


def get_config_values() -> Tuple[str, str, str]:
    """Get configuration values from config file or defaults.

    Returns:
        tuple: (ollama_host, model_name, prompt_message)
    """
    # Default values
    default_host = "http://localhost:11434"
    default_model = "llama3.2"
    default_prompt = (
        "You are an AI assistant that generates philosophical commit messages in the style of Albert Camus.\n"
        "Your task is to analyze git changes and create a commit message that reflects on the absurdity, rebellion, and human condition.\n\n"
        "Git Diff:\n{diff}\n\nGit Status:\n{status}\n\n"
        "Generate a philosophical commit message that:\n"
        "1. Reflects on the nature of the changes made\n"
        "2. Incorporates themes of existentialism and the absurd\n"
        "3. Is concise but meaningful (max 150 characters)\n"
        "4. Avoids technical jargon in favor of philosophical reflection\n\n"
        "Respond with only the commit message, no explanations or additional text."
    )

    try:
        ollama_host = settings.ollama.host
        model_name = settings.run.model_name
        prompt_message = settings.run.prompt_message
    except Exception:
        ollama_host = default_host
        model_name = default_model
        prompt_message = default_prompt

    # Environment variables take precedence
    ollama_host = os.environ.get("OLLAMA_HOST", ollama_host)
    model_name = os.environ.get("OLLAMA_MODEL", model_name)

    return ollama_host, model_name, prompt_message
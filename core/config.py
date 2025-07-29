from pydantic import BaseModel
from pydantic_settings import BaseSettings


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    model_name: str = "llama3:70b"  # Default model name for Ollama
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
    prefix: str = "/api"


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()


settings = Settings()

# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# Install git (for git diff/status)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Optional: Mount a custom config file at runtime
# Example: docker run -v $(pwd)/my_config.toml:/app/config.toml git-camus

# Copy source
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir .

# Default environment variable for model (can be overridden)
ENV OLLAMA_MODEL=llama3:70b

# Entrypoint for git-camus
ENTRYPOINT ["git-camus"]
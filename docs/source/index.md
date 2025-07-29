# Git-Camus: Craft Git Commit Messages with Existential Flair

**git-camus** transforms your Git commit messages into philosophical reflections inspired by the works of [Albert Camus](https://en.wikipedia.org/wiki/Albert_Camus). Instead of mundane messages, each commit becomes a thoughtful meditation on absurdity, rebellion, and the human condition.

## Quick Start

1. **Install Ollama**:
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Start Ollama and pull a model**:
   ```bash
   ollama serve
   ollama pull llama3.2
   ```

3. **Install git-camus**:
   ```bash
   pip install git-camus
   ```

4. **Use it**:
   ```bash
   git add .
   git-camus
   ```

## Features

- **Philosophical Commit Messages**: Transform mundane commits into existential reflections
- **Local Processing**: All AI processing happens locally with Ollama
- **Privacy-First**: No data sent to external services
- **Customizable**: Choose your preferred model and settings
- **Easy Integration**: Works as a drop-in replacement for `git commit`

## Configuration

Set environment variables for customization:

```bash
export OLLAMA_HOST="http://localhost:11434"  # Default Ollama host
export OLLAMA_MODEL="llama3.2"               # Model to use
```

## Examples

- "Refactor authentication: in the face of the absurd, we must persist"
- "Fix pagination logic, acknowledging the futility of infinite scrolling"
- "Add unit tests, for in testing we confront our code's mortality"

---

*"One must imagine Sisyphus committing code."*

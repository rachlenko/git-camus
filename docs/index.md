# Git-Camus Documentation

Welcome to the Git-Camus documentation! This guide will help you understand how to use Git-Camus to transform your mundane Git commit messages into philosophical reflections inspired by Albert Camus.

## What is Git-Camus?

Git-Camus is a command-line tool that analyzes your Git changes and generates philosophical commit messages inspired by existentialist philosophy. Instead of boring commit messages like "Fix bug" or "Add feature", Git-Camus creates thoughtful reflections on the nature of your code changes.

## Key Features

- **🤖 Local AI Processing**: Uses Ollama for privacy-focused, local AI generation
- **📝 Philosophical Commit Messages**: Generate existentialist reflections on your code changes
- **🔒 Privacy First**: No data sent to external services - everything stays on your machine
- **⚡ Fast & Efficient**: Lightweight with minimal dependencies
- **🎯 Contextual**: Analyzes your actual code changes for relevant messages
- **🛠️ Customizable**: Choose your preferred Ollama model and settings

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

3. **Install Git-Camus**:
   ```bash
   pip install git-camus
   ```

4. **Use it**:
   ```bash
   git add .
   git-camus
   ```

## Examples

Instead of:
- `"Fix authentication bug"`
- `"Add user validation"`
- `"Update documentation"`

Git-Camus generates:
- `"In the face of authentication's absurdity, we persist with validation"`
- `"Confronting the human condition through user validation"`
- `"Documentation: maps for navigating our digital Sisyphean task"`

## Documentation Sections

### Getting Started
- [Installation Guide](installation.md) - Detailed setup instructions
- [Quick Start](quickstart.md) - Get up and running in minutes
- [Configuration](configuration.md) - Customize Git-Camus behavior

### Usage
- [Basic Usage](usage.md) - Learn the fundamentals
- [Advanced Usage](advanced.md) - Explore advanced features
- [Examples](examples.md) - See Git-Camus in action

### Development
- [API Reference](api.md) - Complete API documentation
- [Contributing](contributing.md) - How to contribute to Git-Camus
- [Development Guide](development.md) - Set up development environment

### Reference
- [Command Line Interface](cli.md) - All available commands and options
- [Configuration Reference](config.md) - Configuration file format
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

## Philosophy

Git-Camus is inspired by the works of Albert Camus, particularly his concept of the absurd and the human condition. Each commit message reflects on the nature of the changes made, incorporating themes of:

- **Absurdity**: The inherent meaninglessness of certain tasks
- **Rebellion**: The human spirit's refusal to accept meaninglessness
- **Persistence**: The determination to continue despite challenges
- **Human Condition**: The universal experiences of creation and change

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/rachlenko/git-camus/issues)
- **Discussions**: [Join the community](https://github.com/rachlenko/git-camus/discussions)
- **Documentation**: This site and the [README](https://github.com/rachlenko/git-camus)

---

*"One must imagine Sisyphus committing code."* - Albert Camus (probably)
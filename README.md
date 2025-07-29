# Git-Camus: Craft Git Commit Messages with Existential Flair

[![PyPI version](https://badge.fury.io/py/git-camus.svg)](https://badge.fury.io/py/git-camus)
[![Python versions](https://img.shields.io/pypi/pyversions/git-camus.svg)](https://pypi.org/project/git-camus/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Tests](https://github.com/rachlenko/git-camus/actions/workflows/tests.yml/badge.svg)](https://github.com/rachlenko/git-camus/actions/workflows/tests.yml)
[![Coverage](https://codecov.io/gh/rachlenko/git-camus/branch/main/graph/badge.svg)](https://codecov.io/gh/rachlenko/git-camus)
[![Documentation](https://readthedocs.org/projects/git-camus/badge/?version=latest)](https://git-camus.readthedocs.io/)

**Transform your mundane Git commit messages into philosophical reflections inspired by Albert Camus, powered by local AI processing with Ollama.**

## 🌟 Features

- **🤖 Local AI Processing**: Uses Ollama for privacy-focused, local AI generation
- **📝 Philosophical Commit Messages**: Generate existentialist reflections on your code changes
- **🔒 Privacy First**: No data sent to external services - everything stays on your machine
- **⚡ Fast & Efficient**: Lightweight with minimal dependencies
- **🎯 Contextual**: Analyzes your actual code changes for relevant messages
- **🛠️ Customizable**: Choose your preferred Ollama model and settings
- **📚 Well Documented**: Comprehensive documentation and examples

## 🚀 Quick Start

### 1. Install Ollama

```bash
# macOS and Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### 2. Start Ollama and Pull a Model

```bash
# Start the Ollama service
ollama serve

# In another terminal, pull a model
ollama pull llama3.2
```

### 3. Install Git-Camus

```bash
pip install git-camus
```

### 4. Use It!

```bash
# Stage your changes
git add .

# Generate a philosophical commit message
git-camus
```

## 📖 Examples

Instead of boring commit messages like:
- `"Fix bug in authentication"`
- `"Add user validation"`
- `"Update documentation"`

Git-Camus generates philosophical reflections like:
- `"In the face of authentication's absurdity, we persist with validation"`
- `"Confronting the human condition through user validation"`
- `"Documentation: maps for navigating our digital Sisyphean task"`

## 🛠️ Installation

### From PyPI (Recommended)

```bash
pip install git-camus
```

### From Source

```bash
git clone https://github.com/rachlenko/git-camus.git
cd git-camus
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/rachlenko/git-camus.git
cd git-camus
pip install -e ".[dev]"
```

## 🐳 Docker

You can build and run Git-Camus in a Docker container:

```bash
# Build the Docker image
sudo docker build -t git-camus .

# Run with Ollama model (default: llama3:70b)
sudo docker run --rm -it \
  -v $(pwd):/repo \
  -e OLLAMA_MODEL=llama3:70b \
  git-camus
```

You can also mount a custom config file:

```bash
sudo docker run --rm -it \
  -v $(pwd):/repo \
  -v $(pwd)/your_config.toml:/app/config.toml \
  git-camus
```

## ⚙️ Configuration

You can configure the Ollama model name in two ways:

1. **Environment variable**: `OLLAMA_MODEL` (takes precedence)
2. **Config file**: Edit `core/config.py` or provide a compatible config file with a `model_name` field under `[run]`.

### Environment Variables

```bash
# Ollama service URL (default: http://localhost:11434)
export OLLAMA_HOST="http://localhost:11434"

# Model to use (default: llama3.2)
export OLLAMA_MODEL="llama3.2"
```

### Configuration File

Create a `.git-camus.toml` file in your project root:

```toml
[ollama]
host = "http://localhost:11434"
model = "llama3.2"

[generation]
temperature = 0.7
max_tokens = 150
```

## 📖 Usage

### Basic Usage

```bash
# Stage your changes first
git add .

# Generate and commit with a philosophical message
git-camus
```

### Show Message Without Committing

```bash
git-camus --show
```

### Provide Context

```bash
git-camus --message "Fix authentication bug"
```

### Command Line Options

```bash
git-camus [OPTIONS]

Options:
  -s, --show          Show the generated message without committing
  -m, --message TEXT  Original commit message to enhance with Camus-style existentialism
  --help              Show this message and exit
```

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install -e ".[test]"

# Run tests
pytest

# Run with coverage
pytest --cov=git_camus --cov-report=html
```

## 🔧 Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/rachlenko/git-camus.git
cd git-camus

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Code Quality

```bash
# Format code
black .
ruff check --fix .

# Type checking
mypy git_camus/

# Run tests
pytest
```

## 📚 Documentation

- **[Full Documentation](https://git-camus.readthedocs.io/)** - Comprehensive guides and API reference
- **[Installation Guide](https://git-camus.readthedocs.io/en/latest/installation.html)** - Detailed setup instructions
- **[API Reference](https://git-camus.readthedocs.io/en/latest/api.html)** - Complete API documentation
- **[Examples](https://git-camus.readthedocs.io/en/latest/examples.html)** - Usage examples and patterns

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `pytest`
5. Commit your changes: `git-camus -m "Add amazing feature"`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Albert Camus** for the philosophical inspiration
- **Ollama** for providing excellent local AI capabilities
- **The open source community** for the amazing tools that make this possible

## 📊 Project Status

- **Version**: 0.2.0
- **Status**: Beta
- **Python Support**: 3.9+
- **License**: MIT

## 🔗 Links

- **Homepage**: https://github.com/rachlenko/git-camus
- **Documentation**: https://git-camus.readthedocs.io/
- **PyPI**: https://pypi.org/project/git-camus/
- **Issues**: https://github.com/rachlenko/git-camus/issues
- **Discussions**: https://github.com/rachlenko/git-camus/discussions

---

*"One must imagine Sisyphus committing code."* - Albert Camus (probably)

<div align="center">
  <sub>Built with ❤️ and existentialism</sub>
</div>


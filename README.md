# Git-Camus: Craft Git Commit Messages with Existential Flair
![git-camus](docs/images/git-camus_logo.jpeg)

[![PyPI version](https://badge.fury.io/py/git-camus.svg)](https://badge.fury.io/py/git-camus)
[![Python versions](https://img.shields.io/pypi/pyversions/git-camus.svg)](https://pypi.org/project/git-camus/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CI/CD](https://github.com/rachlenko/git-camus/actions/workflows/ci.yml/badge.svg)](https://github.com/rachlenko/git-camus/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/rachlenko/git-camus/branch/main/graph/badge.svg)](https://codecov.io/gh/rachlenko/git-camus)
[![Documentation](https://readthedocs.org/projects/git-camus/badge/?version=latest)](https://git-camus.readthedocs.io/)
[![Docker](https://img.shields.io/docker/pulls/rachlenko/git-camus.svg)](https://hub.docker.com/r/rachlenko/git-camus)

**Transform your mundane Git commit messages into philosophical reflections inspired by Albert Camus, powered by local AI processing with Ollama.**

## 🌟 Features

- **🤖 Local AI Processing**: Uses Ollama for privacy-focused, local AI generation
- **📝 Philosophical Commit Messages**: Generate existentialist reflections on your code changes
- **🔒 Privacy First**: No data sent to external services - everything stays on your machine
- **⚡ Fast & Efficient**: Lightweight with minimal dependencies
- **🎯 Contextual**: Analyzes your actual code changes for relevant messages
- **🛠️ Customizable**: Choose your preferred Ollama model and settings
- **📚 Well Documented**: Comprehensive documentation and examples
- **🐳 Container Ready**: Docker and Kubernetes deployment support
- **🚀 Production Ready**: Professional CI/CD pipeline and monitoring

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

#### Option A: Using pip (Recommended)

```bash
pip install git-camus
```

#### Option B: Using the Installation Script

```bash
# Download and run the installation script
curl -fsSL https://raw.githubusercontent.com/rachlenko/git-camus/main/install.sh | bash
```

#### Option C: From Source (Development)

```bash
git clone https://github.com/rachlenko/git-camus.git
cd git-camus
./scripts/setup-dev.sh
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

## ⚙️ Configuration

Git-Camus can be configured through environment variables or a configuration file.

### Environment Variables

```bash
# Ollama service URL (default: http://localhost:11434)
export OLLAMA_HOST="http://localhost:11434"

# Model to use (default: llama3.2)
export OLLAMA_MODEL="llama3.2"
```

### Configuration File

Create a `config.yaml` file in your project root:

```yaml
ollama:
  host: "http://localhost:11434"
  model: "llama3.2"
run:
  prompt_message: |
    You are an AI assistant that generates philosophical commit messages in the style of Albert Camus.
    Your task is to analyze git changes and create a commit message that reflects on the absurdity, rebellion, and human condition.
```

Environment variables take precedence over configuration file settings.

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

## 🐳 Docker Deployment

### Quick Start with Docker Compose

```bash
# Clone the repository
git clone https://github.com/rachlenko/git-camus.git
cd git-camus

# Start the stack (includes Ollama server)
docker-compose -f docker/docker-compose.yml up -d

# Use git-camus in development container
docker-compose -f docker/docker-compose.yml exec git-camus-dev git-camus --help
```

### Production Docker Image

```bash
# Pull the latest image
docker pull ghcr.io/rachlenko/git-camus:latest

# Run with your local git repository
docker run --rm -it \
  -v $(pwd):/workspace \
  -e OLLAMA_HOST=http://your-ollama-server:11434 \
  ghcr.io/rachlenko/git-camus:latest
```

### Build Custom Image

```bash
# Build production image
./scripts/docker-build.sh git-camus latest

# Build development image
docker build -f docker/Dockerfile.dev -t git-camus:dev .
```

## ☸️ Kubernetes Deployment

### Quick Deploy with Helm

```bash
# Add the Helm chart repository (when published)
helm repo add git-camus https://rachlenko.github.io/git-camus

# Install for development
helm install git-camus git-camus/git-camus \
  --namespace git-camus --create-namespace \
  --values helm/values-dev.yaml

# Install for production
helm install git-camus git-camus/git-camus \
  --namespace git-camus --create-namespace \
  --values helm/values-prod.yaml
```

### Manual Deployment

```bash
# Deploy to development environment
./scripts/deploy.sh dev git-camus-dev

# Deploy to production environment
./scripts/deploy.sh prod git-camus-prod

# Check deployment status
kubectl get pods -n git-camus-prod
```

## 🧪 Testing

### Run Tests Locally

```bash
# Setup development environment
./scripts/setup-dev.sh

# Run all tests
./scripts/test.sh

# Run specific test categories
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests  
pytest tests/e2e/          # End-to-end tests
```

### Test Coverage

```bash
# Generate coverage report
pytest --cov=git_camus --cov-report=html --cov-report=term-missing

# View HTML report
open htmlcov/index.html
```

## 🔧 Development

### Professional Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/rachlenko/git-camus.git
cd git-camus
./scripts/setup-dev.sh

# Activate virtual environment
source venv/bin/activate

# Run development checks
./scripts/test.sh        # Run all tests
./scripts/build.sh       # Build package
```

### Project Structure

```
git-camus/
├── src/git_camus/           # Source code (src layout)
│   ├── core/                # Core business logic
│   ├── cli/                 # Command line interface  
│   └── utils/               # Utility functions
├── tests/                   # Comprehensive test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── e2e/               # End-to-end tests
├── .github/workflows/      # CI/CD automation
├── docker/                 # Container configurations
├── helm/                   # Kubernetes deployment charts
├── scripts/               # Development automation
└── requirements/          # Dependency management
```

### Code Quality Standards

```bash
# Code formatting and linting
ruff check src/ tests/      # Fast Python linter
ruff format src/ tests/     # Code formatting
black src/ tests/           # Alternative formatting

# Type checking
mypy src/                   # Static type checking

# Security scanning  
bandit -r src/             # Security vulnerability scanning
safety check               # Dependency vulnerability check
```

### CI/CD Pipeline

The project includes a comprehensive CI/CD pipeline that:

- **Multi-Platform Testing**: Linux, Windows, macOS
- **Python Compatibility**: 3.9, 3.10, 3.11, 3.12, 3.13
- **Security Scanning**: Bandit, Safety
- **Docker Multi-Arch**: AMD64, ARM64
- **Automated Releases**: PyPI publishing
- **Container Registry**: GitHub Container Registry

## 📚 Documentation

- **[Full Documentation](https://git-camus.readthedocs.io/)** - Comprehensive guides and API reference
- **[Installation Guide](docs/source/installation.md)** - Detailed setup instructions
- **[API Reference](docs/source/api.md)** - Complete API documentation
- **[Docker Guide](docker/README.md)** - Container deployment guide
- **[Kubernetes Guide](helm/README.md)** - K8s deployment documentation

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Setup development environment: `./scripts/setup-dev.sh`
4. Make your changes
5. Run tests: `./scripts/test.sh`
6. Build package: `./scripts/build.sh`
7. Commit your changes: `git-camus -m "Add amazing feature"`
8. Push to the branch: `git push origin feature/amazing-feature`
9. Open a Pull Request

### Automated Quality Checks

All contributions are automatically tested with:
- **Code quality**: Ruff, Black, MyPy
- **Security**: Bandit, Safety
- **Testing**: Pytest with >95% coverage
- **Multi-platform**: Linux, Windows, macOS
- **Container**: Docker build verification

## 🏭 Production Usage

### Deployment Options

- **🐳 Docker**: Single container deployment
- **☸️ Kubernetes**: Scalable container orchestration
- **📦 PyPI**: Direct pip installation
- **🔧 Source**: Development and customization

### Monitoring and Observability

- **Health Checks**: Built-in container health monitoring
- **Metrics**: Prometheus-compatible metrics (planned)
- **Logging**: Structured logging with configurable levels
- **Tracing**: OpenTelemetry support (planned)

### Production Configuration

```yaml
# Production values for Helm deployment
replicaCount: 3
resources:
  limits:
    cpu: 1
    memory: 1Gi
  requests:
    cpu: 200m
    memory: 256Mi
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 20
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Albert Camus** for the philosophical inspiration
- **Ollama** for providing excellent local AI capabilities
- **The open source community** for the amazing tools that make this possible

## 📊 Project Status

- **Version**: 0.2.0
- **Status**: Production Ready
- **Python Support**: 3.9+
- **License**: MIT
- **Container Support**: ✅ Docker, Kubernetes
- **CI/CD**: ✅ GitHub Actions
- **Testing**: ✅ >95% Coverage

## 🔗 Links

- **Homepage**: https://github.com/rachlenko/git-camus
- **Documentation**: https://git-camus.readthedocs.io/
- **PyPI**: https://pypi.org/project/git-camus/
- **Container Registry**: https://ghcr.io/rachlenko/git-camus
- **Issues**: https://github.com/rachlenko/git-camus/issues
- **Discussions**: https://github.com/rachlenko/git-camus/discussions

## 🆘 Support

- **📖 Documentation**: Check our comprehensive docs first
- **🐛 Bug Reports**: Open an issue on GitHub
- **💡 Feature Requests**: Start a discussion
- **💬 Community**: Join GitHub Discussions
- **🔒 Security**: Report vulnerabilities privately

---

*"One must imagine Sisyphus committing code."* - Albert Camus (probably)

<div align="center">
  <sub>Built with ❤️ and existentialism by the open source community</sub>
</div>
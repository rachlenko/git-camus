#!/bin/bash
# Development environment setup script

set -euo pipefail

echo "🛠️  Setting up git-camus development environment..."

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $REQUIRED_VERSION or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python version check passed: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install development dependencies
echo "Installing development dependencies..."
pip install -e ".[dev,test]"

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

# Make scripts executable
echo "Making scripts executable..."
chmod +x scripts/*.sh

echo "✅ Development environment setup completed!"
echo ""
echo "To activate the environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run tests:"
echo "  ./scripts/test.sh"
echo ""
echo "To build the package:"
echo "  ./scripts/build.sh"
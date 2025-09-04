#!/bin/bash
# Test script for git-camus

set -euo pipefail

echo "🧪 Running tests for git-camus..."

# Install test dependencies
echo "Installing test dependencies..."
pip install -e ".[dev,test]"

# Run linting
echo "Running code formatting checks..."
ruff check src/ tests/
ruff format --check src/ tests/

# Run type checking
echo "Running type checks..."
mypy src/

# Run tests with coverage
echo "Running tests with coverage..."
pytest --cov=git_camus --cov-report=term-missing --cov-report=html --cov-report=xml -v

# Security checks
echo "Running security checks..."
if command -v bandit &> /dev/null; then
    bandit -r src/ -f json -o bandit-report.json || true
    bandit -r src/
fi

if command -v safety &> /dev/null; then
    safety check --json --output safety-report.json || true
fi

echo "✅ All tests passed!"
echo "📊 Coverage report available in htmlcov/"
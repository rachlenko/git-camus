#!/bin/bash
# Build script for git-camus

set -euo pipefail

echo "🔨 Building git-camus..."

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Install build dependencies
echo "Installing build dependencies..."
pip install --upgrade build twine

# Build the package
echo "Building package..."
python -m build

# Check the package
echo "Checking package..."
twine check dist/*

echo "✅ Build completed successfully!"
echo "📦 Built packages:"
ls -la dist/
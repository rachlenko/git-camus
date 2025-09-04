#!/bin/bash
# Docker build script for git-camus

set -euo pipefail

IMAGE_NAME=${1:-git-camus}
TAG=${2:-latest}
PLATFORM=${3:-linux/amd64,linux/arm64}

echo "🐳 Building Docker image: $IMAGE_NAME:$TAG"

# Build multi-platform image
echo "Building for platforms: $PLATFORM"
docker buildx build \
    --platform "$PLATFORM" \
    --file docker/Dockerfile \
    --tag "$IMAGE_NAME:$TAG" \
    --push \
    .

echo "✅ Docker image built successfully!"
echo "🏷️  Image: $IMAGE_NAME:$TAG"
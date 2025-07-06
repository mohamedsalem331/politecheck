#!/bin/bash

set -e

IMAGE_NAME="politecheck"
REGISTRY="mohamed331"
TAG="latest"
BUILD_CONTEXT="."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' 

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

# Build full image name
if [[ -n "$REGISTRY" ]]; then
    FULL_IMAGE_NAME="${REGISTRY}/${IMAGE_NAME}:${TAG}"
else
    FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"
fi

print_status "Building Docker image: $FULL_IMAGE_NAME"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_status "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build the image
print_status "Building image..."
docker build -t "$FULL_IMAGE_NAME" "$BUILD_CONTEXT"

if [ $? -eq 0 ]; then
    print_status "✅ Image built successfully!"
    print_status "Image: $FULL_IMAGE_NAME"
    
    # Show image info
    print_status "Image details:"
    docker images "$FULL_IMAGE_NAME"
    
    # Optional: push to registry
    if [[ -n "$REGISTRY" ]]; then
        read -p "Do you want to push the image to registry? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_status "Pushing image to registry..."
            docker push "$FULL_IMAGE_NAME"
            if [ $? -eq 0 ]; then
                print_status "✅ Image pushed successfully!"
            else
                print_status "Failed to push image"
                exit 1
            fi
        fi
    fi
else
    print_status "❌ Failed to build image"
    exit 1
fi 
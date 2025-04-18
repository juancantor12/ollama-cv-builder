#!/bin/bash
set -e  # exit immediately if a command exits with a non-zero status

echo "Installing dependencies..."
make install

echo "Linting code..."
make lint

echo "Checking code formatting..."
make format

echo "Running unit tests..."
make test

echo "Building Docker image..."
make build

echo "Running Docker container..."
make run

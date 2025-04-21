#!/bin/bash
set -e  # exit immediately if a command exits with a non-zero status

URL=$1

echo "Installing dependencies..."
make install

echo "Linting code..."
make lint

echo "Checking code formatting..."
make format

echo "Running unit tests..."
make test

echo "Running the module"
make run URL="$URL"
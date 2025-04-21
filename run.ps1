$ErrorActionPreference = "Stop"

param (
    [string]$URL
)

if (-not $URL) {
    Write-Host "Error: URL argument is required."
    exit 1
}

Write-Host "Installing dependencies..."
pip install -r requirements.txt

Write-Host "Linting code..."
ruff check src/ tests/

Write-Host "Checking formatting..."
black src/ tests/

Write-Host "Running unit tests..."
pytest tests/

Write-Host "Running the app"
python -m resume_generator.cli all $URL

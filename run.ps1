param ([string]$URL)
$ErrorActionPreference = "Stop"

if ($URL) {
    Write-Host "Running the app"
    python -m src.resume_generator.cli all $URL
    exit 0
} else {
    Write-Host "Installing dependencies..."
    pip install -r requirements.txt

    Write-Host "Linting code..."
    ruff check src/ tests/

    Write-Host "Checking formatting..."
    black src/ tests/

    Write-Host "Running unit tests..."
    pytest tests/
}
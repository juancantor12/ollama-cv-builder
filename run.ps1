param (
    [string]$url,        # Url of the offering, if it cannot be accessed using requests the script will fail
    [string]$actions,    # Which actions to aperform, if empty, all are executed
    [switch]$install,
    [switch]$format,
    [switch]$lint,
    [switch]$security,
    [switch]$audit,
    [switch]$test,
    [switch]$precommit,
    [switch]$setup,
    [switch]$help
)
$ErrorActionPreference = "Stop"

function Execute-Action {
    param (
        [string]$action
    )
    Write-Host "$action..."
    switch ($action) {
        "install" { pip install -r requirements.txt }
        "format" { black src/ tests/ }
        "lint" { ruff check src/ tests/ }
        "security" { bandit -r src/ }
        "audit" { pip-audit -r requirements.txt }
        "test" { pytest tests/ -vv }
    }
}

if ($help){
    Write-Host (
        @(
            "Usage:",
            "-url       The URL to fetch the offering data (required for running the app).",
            "-actions   List of actions to perform (dash-separated, no spaces). Defaults to 'all'.",
            "-install   Installs dependencies",
            "-format    Format the code with black.",
            "-lint      Lint the code with ruff.",
            "-security  Check code security with bandit.",
            "-audit     Check dependencies vulnerabilities with pip-audit.",
            "-test      Run unit tests with pytest",
            "-precommit Run format, lint, security, audit and test"
            "-setup     Run install, format, lint, security, audit and test.",
            "-help      Show this help message."
            "",
            "Availabe actions: fetch, summarize, tailor, generate, all",
            "If no actions are provided, all will run",
            "",
            "Example: .\\run.ps1 -url https://www.example.com -actions fetch-summarize-tailor-generate"
        ) -join [Environment]::NewLine
    )
    exit 0
}

if ($install) { Execute-Action -action "install"; exit }
if ($format) { Execute-Action -action "format"; exit }
if ($lint) { Execute-Action -action "lint"; exit }
if ($security) { Execute-Action -action "security"; exit }
if ($audit) { Execute-Action -action "audit"; exit }
if ($test) { Execute-Action -action "test"; exit }
if ($precommit) { 
    "format", "lint", "security", "audit", "test" | ForEach-Object { Execute-Action -action $_ }
    exit
}
if ($setup) { 
    "install", "format", "lint", "security", "audit", "test" | ForEach-Object { Execute-Action -action $_ }
    exit
}

if ($URL) {
    Write-Host "Running the app"
    $script_action = "all"
    if($actions){
        $script_action = $actions
    }
    python -m src.resume_generator.cli --url $url --actions $script_action
    exit 0
}
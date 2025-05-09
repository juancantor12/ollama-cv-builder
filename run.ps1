param (
    [string]$url,        # Url of the offering, if it cannot be accessed using requests the script will fail
    [string]$actions,    # Which actions to aperform, if empty, all are executed
    [switch]$help,
    [switch]$setup,
    [switch]$install,
    [switch]$lint,
    [switch]$format,
    [switch]$test

)
$ErrorActionPreference = "Stop"

function fn_install {
    Write-Host "Installing dependencies..."
    pip install -r requirements.txt
}

function fn_lint {
    Write-Host "Linting code..."
    ruff check src/ tests/
}

function fn_format {
    Write-Host "Checking format..."
    black src/ tests/
}

function fn_test {
    Write-Host "Running unit tests..."
    pytest tests/ -vv
}

function fn_setup {
    fn_install
    fn_format
    fn_lint
    fn_test
}

if ($help){
    Write-Host (
        @(
            "Usage:",
            "-url      {str}  The url to fetch the offering data",
            "-actions  {list[str]}   The list of actions to perform (in given order, dash (-) sepparated, no spaces)",
            "-help     Prints help information",
            "-setup    Install, formats, lints and test",
            "-install  Installs dependencies",
            "-lint     Lint the code with ruff",
            "-format   Format the code with black",
            "-test     Runs unit testing with pytest",
            "",
            "Availabe actions: fetch, summarize, tailor, generate, all",
            "If no actions are provided, all will run",
            "",
            "Example: .\\run.ps1 -url https://www.example.com -actions fetch-summarize-tailor-generate"
        ) -join [Environment]::NewLine
    )
    exit 0
}

if ($install) { 
    fn_install
    exit 0
}

if ($lint) {
    fn_lint
    exit 0
}

if ($format) {
    fn_format
    exit 0
}

if ($test) {
    fn_test
    exit 0
}

if ($setup) {
    fn_setup
    exit 0
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
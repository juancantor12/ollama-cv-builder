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

function Execute-Action {
    param (
        [string]$action
    )
    Write-Host "$action..."
    switch ($action) {
        "install" { pip install -r requirements.txt }
        "lint" { ruff check src/ tests/ }
        "format" { black src/ tests/ }
        "test" { pytest tests/ -vv }
    }
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

if ($install) { Execute-Action -action "install"; exit }
if ($lint) { Execute-Action -action "lint"; exit }
if ($format) { Execute-Action -action "format"; exit }
if ($test) { Execute-Action -action "test"; exit }
if ($setup) { 
    "install", "format", "lint", "test" | ForEach-Object { Execute-Action -action $_ }
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
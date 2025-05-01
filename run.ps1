param (
	[string]$url,	   # Url of the offering, if it cannot be accessed using requests the script will fail
	[string]$actions,   # Which actions to aperform, if empty, all are executed
	[switch]$help
)
$ErrorActionPreference = "Stop"
if ($help -or !$url -and !$actions){
	Write-Host (
		@(
			"Usage:",
			"-url	   The url to fetch the offering data",
			"-actions   The list of actions to perform (in given order, dash (-) sepparated, no spaces)",
			"-help	  Prints help information",
			"Availabe actions: fetch, summarize, tailor, generate, all",
			"If no actions are provided, all will run",
			"If no URL is provided, the script will execute the setup (install requirements, lint, format, unit testing)",
            "Example: .\\run.ps1 -url https://www.example.com -actions summarize-tailor-generate"
		) -join [Environment]::NewLine
	)
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
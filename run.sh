#!/bin/bash
set -e  # Exit immediately if any command exits with a non-zero status
function show_help() {
    echo "Usage:"
    echo "-url      {str}  The URL to fetch the offering data (required for running the app)"
    echo "-actions  {str}  List of actions to perform (dash-separated, no spaces). Defaults to 'all'."
    echo "-install  Installs dependencies."
    echo "-lint     Lint the code with ruff."
    echo "-format   Format the code with black."
    echo "-test     Run unit testing with pytest."
    echo "-setup    Run install, format, lint, and test."
    echo "-help     Show this help message."
    echo ""
    echo "Availabe actions: fetch, summarize, tailor, generate, all",
    echo ""
    echo "Example: ./run.sh -url https://example.com -actions fetch-summarize-tailor"
    exit 0
}

execute_action() {
    setup_steps=("install" "lint" "format" "test")
    case $1 in
        "-install") pip install -r requirements.txt ;;
        "-lint") ruff check src/ tests/ ;;
        "-format") black src/ tests/ ;;
        "-test") pytest tests/ -vv ;;
	"-setup")
	    for step in setup_steps; do
		execute_action "$arg"
	    done
	 ;;
	"-help") show_help 
    esac
}

# Parse the arguments
for arg in "$@"; do
    case "$arg" in
        -*) 
            execute_action "$arg"
            exit 0
            ;;
    esac
done

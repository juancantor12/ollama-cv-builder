#!/bin/bash
set -e  # Exit immediately if any command exits with a non-zero status
function show_help() {
    echo "Usage:"
    echo "-url      The URL to fetch the offering data (required for running the app)."
    echo "-actions  List of actions to perform (dash-separated, no spaces). Defaults to 'all'."
    echo "-install  Installs dependencies."
    echo "-format   Format the code with black."
    echo "-lint     Lint the code with ruff."
    echo "-security Check code security with bandit."
    echo "-audit    Check dependencies vulnerabilities with pip-audit."
    echo "-test     Run unit tests with pytest."
    echo "-setup    Run install, format, lint, security, audit and test."
    echo "-help     Show this help message."
    echo ""
    echo "Availabe actions: fetch, summarize, tailor, generate, all",
    echo ""
    echo "Example: ./run.sh -url https://example.com -actions fetch-summarize-tailor"
    exit 0
}

execute_action() {
    setup_steps=("-install" "-lint" "-format" "-test")
    case $1 in
        "-install") make install-dependencies ;;
        "-format") make format-code ;;
        "-lint") make lint-code ;;
        "-security") make check-code-security ;;
        "-audit") make check-dependencies-vulnerabilities ;;
        "-test") make unit-testing ;;
	"-setup")
	    for step in "${setup_steps[@]}"; do
		execute_action "$step"
	    done
	 ;;
	"-help") show_help 
    esac
}

if [ "$1" = "-url" ]; then
    if [ -z "$2" ]; then
	echo "-url parameter provided but no url value found."
	exit 1
    elif [ -z "$3" -o "$3" != "-actions" ]; then
	python -m src.resume_generator.cli --url "$2" --actions all
	exit 0
    elif [ -n "$3" -a "$3" = "-actions" -a -n "$4" ]; then
	python -m src.resume_generator.cli --url "$2" --actions "$4"
	exit 0
    fi
fi

# Other params
for arg in "$@"; do
    case "$arg" in
        -*) 
            execute_action "$arg"
            exit 0
            ;;
    esac
done

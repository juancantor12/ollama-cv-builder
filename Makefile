.PHONY: install lint format test run all

install:
	pip install -r requirements.txt

lint:
	ruff check src/ tests/

format:
	black src/ tests/

test:
	pytest tests/

run:
	@if [ -z "$(URL)" ]; then \
		echo "Error: URL is required for the 'run' target."; \
		exit 1; \
	fi
	python -m resume_generator.cli all $(URL)

all:
	install lint format test run
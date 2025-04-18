.PHONY: install lint format test build run

install:
	pip install -r requirements.txt

lint:
	ruff check src/ tests/

format:
	black src/ tests/

test:
	pytest tests/
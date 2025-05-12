# .PHONY: install lint format test run all

# install:
# 	pip install -r requirements.txt

# lint:
# 	ruff check src/ tests/

# format:
# 	black src/ tests/

# test:
# 	pytest tests/

# run:
# 	@if [ -z "$(URL)" ]; then \
# 		echo "Error: URL is required for the 'run' target."; \
# 		exit 1; \
# 	fi
# 	python -m resume_generator.cli all $(URL)

# all:
# 	install lint format test run

# .PHONY specifies names that are to be treated as commands and not files
.PHONY: install lint format test run setup all

ACTIONS ?= all # ?= assigns a default value if the variable hasn't been set before

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

lint:
	@echo "Linting code..."
	ruff check src/ tests/

format:
	@echo "Formatting code..."
	black src/ tests/

test:
	@echo "Running tests..."
	pytest tests/ -vv

run:
	@echo "Running with actions: $(ACTIONS)"
	@if [ -z "$(URL)" ]; then \
		echo "Error: URL is required for the 'run' action."; \
		exit 1; \
	fi
	python -m src.resume_generator.cli --url $(URL) --actions $(ACTIONS)

setup: install format lint test

# all: setup run

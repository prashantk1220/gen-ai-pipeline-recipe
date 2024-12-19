.PHONY: help install tests run clean clean-all all


VENV_DIR = venv
VENV_PATH = venv/bin

clean: ## Clean up Python cache and test artifacts
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage

clean-all: clean ## Clean up Python cache and installed deps
	rm -rf $(VENV_DIR)

install: ## Install required Python dependencies into $(VENV_DIR)
	if [ ! -d "$(VENV_DIR)" ]; then \
		python3.12 -m venv $(VENV_DIR); \
	fi
	$(VENV_PATH)/pip install -U pip setuptools
	$(VENV_PATH)/pip install poetry
	$(VENV_PATH)/poetry install


tests: ## Run all the tests in tests package using pytest
	$(VENV_PATH)/poetry run pytest

run: ## Start the fastapi application
	$(VENV_PATH)/poetry run start


all: clean-all install test run

help: ## Display this help message
	@echo "Usage: make [target]"
	@echo
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

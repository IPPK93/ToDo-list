TESTS = tests

VENV ?= .venv
ifeq ($(OS), Windows_NT)
	BIN_PATH = $(VENV)/Scripts
else
	BIN_PATH = $(VENV)/bin
endif
CODE = tests app

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: venv
venv:
	python -m venv $(VENV)
	$(BIN_PATH)/python -m pip install --upgrade pip
	$(BIN_PATH)/python -m pip install poetry
	$(BIN_PATH)/poetry install

.PHONY: test
test: ## Runs pytest
	$(BIN_PATH)/pytest -v tests

.PHONY: lint
lint: ## Lint code
	$(BIN_PATH)/flake8 --jobs 4 --statistics --show-source $(CODE)
	$(BIN_PATH)/pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	$(BIN_PATH)/mypy $(CODE)
	$(BIN_PATH)/black --skip-string-normalization --check $(CODE)

.PHONY: format
format: ## Formats all files
	$(BIN_PATH)/isort $(CODE)
	$(BIN_PATH)/black --skip-string-normalization $(CODE)
	$(BIN_PATH)/autoflake --recursive --in-place --remove-all-unused-imports $(CODE)
	$(BIN_PATH)/unify --in-place --recursive $(CODE)

.PHONY: check
check: format lint test

.PHONY: up
up:
	FLASK_APP=app.py
	$(BIN_PATH)/flask run

.PHONY: ci
ci:	lint test ## Lint code then run tests

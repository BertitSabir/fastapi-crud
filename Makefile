ifdef OS
	PYTHON ?= .venv\Scripts\python.exe
else
	ifeq ($(shell printenv | grep -o '^DOCKER=.*'), DOCKER=1)
		PYTHON ?= python
	else
		PYTHON ?= .venv/bin/python
		export PYTHONPATH := $(PYTHONPATH):$(PROJECT_ROOT_DIR)
	endif
endif

SETTINGS_FILENAME = pyproject.toml

PHONY = help install install-dev test test-module sync-target-table sync-target-tables sync-target-table-mp sync-target-tables-mp test-cov test-cov-ci

help:
	@echo "---------------HELP-----------------"
	@echo "To install the project type -> make install"
	@echo "To install the project for development type -> make install-dev"
	@echo "To test the project type -> make test"
	@echo "------------------------------------"

install:
	uv sync

install-dev:
	uv sync --group dev

test:
	uv run pytest --cov=src/ --cov-report=term-missing --cov-report=html tests/

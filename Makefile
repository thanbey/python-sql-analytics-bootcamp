.PHONY: create_environment requirements jupyter assess lint format clean tableau help

#################################################################################
# GLOBALS                                                                        #
#################################################################################

PROJECT_NAME = analytics-bootcamp
PYTHON_VERSION := $(shell python --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)

#################################################################################
# COMMANDS                                                                       #
#################################################################################

## Create a virtual environment using uv
create_environment:
	uv venv --python $(PYTHON_VERSION)
	@echo ">>> Virtual environment created at .venv/"
	@echo ">>> Activate with: source .venv/bin/activate  (Mac/Linux)"
	@echo ">>>             or: .venv\\Scripts\\activate   (Windows)"

## Install Python dependencies using uv
requirements:
	uv pip install -r requirements.txt
	uv pip install -e .
	@echo ">>> Dependencies installed. analytics_bootcamp module is importable."

## Launch Jupyter notebook server
jupyter:
	jupyter notebook notebooks/

## Start at the assessment
assess:
	jupyter notebook notebooks/0.0-assessment/0.1-assessment-python-pandas.ipynb

## Lint Python source files
lint:
	uv run flake8 analytics_bootcamp/
	uv run black --check analytics_bootcamp/

## Auto-format Python source files
format:
	uv run black analytics_bootcamp/
	uv run isort analytics_bootcamp/

## Delete compiled Python files and Jupyter checkpoints
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
	@echo ">>> Cleaned up compiled files and checkpoints."

## tableau : Generate Tableau .hyper extract files in data/tableau/
tableau:
	uv run python scripts/generate_hyper_files.py

## Show this help
help:
	@echo ""
	@echo "Available make targets:"
	@echo "  create_environment  Create a Python $(PYTHON_VERSION) virtual environment (uv)"
	@echo "  requirements        Install dependencies via uv + install analytics_bootcamp"
	@echo "  jupyter             Launch Jupyter in notebooks/"
	@echo "  assess              Open the assessment notebook directly"
	@echo "  lint                flake8 + black check (via uv run)"
	@echo "  format              Auto-format with black + isort (via uv run)"
	@echo "  clean               Remove .pyc files and Jupyter checkpoints"
	@echo ""

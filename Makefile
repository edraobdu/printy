MAKEFLAGS += --no-print-directory --silent

.PHONY: help test test-cov clean build-dist install-local publish-test publish show-version bump-patch bump-minor bump-major sync uv-install setup test-compat

.DEFAULT_GOAL := help

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Testing commands (using unittest, NOT pytest)
test:  ## Run all tests with coverage
	uv run coverage run -m unittest discover -s tests -v
	uv run coverage report

test-cov:  ## Run tests with HTML coverage report
	uv run coverage run -m unittest discover -s tests -v
	uv run coverage html
	uv run coverage report
	@echo "Coverage report: htmlcov/index.html"

clean:  ## Remove build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Version management
show-version:  ## Show current version from pyproject.toml
	@uv version

bump-patch:  ## Bump patch version (0.1.1 -> 0.1.2)
	@uv version --bump patch

bump-minor:  ## Bump minor version (0.1.1 -> 0.2.0)
	@uv version --bump minor

bump-major:  ## Bump major version (0.1.1 -> 1.0.0)
	@uv version --bump major

# Python package building and publishing
build-dist: clean  ## Build Python distribution packages (wheel + sdist)
	@echo "Building distribution packages..."
	uv build
	@echo "Build complete! Packages in dist/"
	@ls -lh dist/

install-local: build-dist  ## Install package locally from built wheel
	@echo "Installing from local build..."
	uv pip install dist/*.whl --force-reinstall
	@echo "Installation complete!"

publish-test: build-dist  ## Publish to TestPyPI for testing
	@echo "Publishing to TestPyPI..."
	uv publish --publish-url https://test.pypi.org/legacy/
	@echo "Published to TestPyPI! Install with:"
	@echo "  pip install --index-url https://test.pypi.org/simple/ printy"

publish: test build-dist  ## Publish to production PyPI (requires confirmation)
	@echo "WARNING: This will publish to production PyPI!"
	@read -p "Version $$(grep '^version = ' pyproject.toml | cut -d'"' -f2) - Continue? [y/N] " confirm && \
	[ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ] || (echo "Aborted." && exit 1)
	@echo "Publishing to PyPI..."
	uv publish
	@echo "Published! Install with: pip install printy"

# Local development with uv
uv-install:  ## Install uv (one-time setup)
	curl -LsSf https://astral.sh/uv/install.sh | sh

sync:  ## Sync dependencies with uv (local development)
	uv sync --all-extras

test-compat:  ## Test compatibility across Python versions
	@echo "Testing Python 3.10..."
	@uv run --python 3.10 python --version || echo "Python 3.10 not available"
	@echo "Testing Python 3.13..."
	@uv run --python 3.13 python --version || echo "Python 3.13 not available"
	@echo "Testing Python 3.14..."
	@uv run --python 3.14 python --version || echo "Python 3.14 not available"

setup:  ## One-time local development setup
	@echo "Setting up local development environment..."
	@command -v uv >/dev/null 2>&1 || (echo "Installing uv..." && curl -LsSf https://astral.sh/uv/install.sh | sh)
	@echo "Installing Python 3.14..."
	uv python install 3.14
	@echo "Syncing dependencies..."
	uv sync --all-extras
	@echo "Installing pre-commit hooks..."
	uv run pre-commit install
	@echo "Setup complete! Virtual environment ready at .venv/"

pre-commit:  ## Run pre-commit hooks on all files
	uv run pre-commit run --all-files

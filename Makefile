# Project information
PROJECT_NAME := inceptor
PACKAGE_NAME := inceptor
PYTHON := python3
PIP := pip
POETRY := $(shell command -v poetry 2> /dev/null || echo "poetry")

# Environment
PYTHON_ENV := .venv
PYTHON_BIN := $(PYTHON_ENV)/bin/python
PIP := $(PYTHON_ENV)/bin/pip

# Development
DEV_PORT := 8000
TEST_PATH := tests/
COVERAGE_REPORT := htmlcov/
DOCKER_COMPOSE := docker-compose

# Colors
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

# Documentation
DOCS_PORT := 8001
DOCS_DIR := docs

# Colors
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

# Helpers
PYTHON_PACKAGES := $(PACKAGE_NAME) tests
PYTHON_FILES := $(shell find $(PYTHON_PACKAGES) -name '*.py' -o -name '*.pyi')

.PHONY: help install install-dev install-deps install-server \
        test lint format check build publish clean clean-all

##@ Help
help:  ## Display this help
	@echo "$(YELLOW)Inceptor - Multi-Level Solution Architecture Generator$(RESET)"
	@echo "\n$(WHITE)Usage: make $(GREEN)<target>$(RESET)"
	@echo "\n$(YELLOW)Available targets:$(RESET)"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-15s$(RESET) %s\n", $$1, $$2 }' $(MAKEFILE_LIST) | sort
	@echo "\n$(YELLOW)Development:$(RESET)"
	@echo "  $(GREEN)install$(RESET)      - Install package in development mode with all dependencies"
	@echo "  $(GREEN)install-dev$(RESET)  - Install development dependencies"
	@echo "  $(GREEN)test$(RESET)         - Run tests quickly with the default Python"
	@echo "  $(GREEN)test-cov$(RESET)     - Run tests with coverage report"
	@echo "  $(GREEN)lint$(RESET)         - Check code style with flake8 and mypy"
	@echo "  $(GREEN)format$(RESET)       - Format code with black and isort"
	@echo "  $(GREEN)check$(RESET)        - Run all checks (lint, test, format)"
	@echo "\n$(YELLOW)Documentation:$(RESET)"
	@echo "  $(GREEN)docs$(RESET)         - Generate documentation"
	@echo "  $(GREEN)serve-docs$(RESET)   - Start documentation server"
	@echo "\n$(YELLOW)Packaging:$(RESET)"
	@echo "  $(GREEN)build$(RESET)        - Build package"
	@echo "  $(GREEN)publish$(RESET)      - Publish package to PyPI"
	@echo "  $(GREEN)release$(RESET)      - Create a new release (bump version, tag, push)"
	@echo "\n$(YELLOW)Cleanup:$(RESET)"
	@echo "  $(GREEN)clean$(RESET)        - Remove build artifacts and Python cache"
	@echo "  $(GREEN)clean-pyc$(RESET)    - Remove Python file artifacts"
	@echo "  $(GREEN)clean-test$(RESET)   - Remove test and coverage artifacts"
	@echo "  $(GREEN)clean-docs$(RESET)   - Remove documentation build artifacts"

##@ Setup
install:  ## Install package in development mode with all dependencies
	@echo "$(YELLOW)Installing package in development mode...$(RESET)"
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install poetry
	$(POETRY) install --with dev --extras "cli server"
	@echo "$(GREEN)✓ Package installed in development mode$(RESET)"

install-dev:  ## Install development dependencies
	@echo "$(YELLOW)Installing development dependencies...$(RESET)"
	$(POETRY) install --with dev
	@echo "$(GREEN)✓ Development dependencies installed$(RESET)"

install-deps:  ## Install runtime dependencies
	@echo "$(YELLOW)Installing runtime dependencies...$(RESET)"
	$(POETRY) install --extras "cli"
	@echo "$(GREEN)✓ Runtime dependencies installed$(RESET)"

install-server:  ## Install server dependencies
	@echo "$(YELLOW)Installing server dependencies...$(RESET)"
	$(POETRY) install --extras "server"
	@echo "$(GREEN)✓ Server dependencies installed$(RESET)"

install-js:  ## Install JavaScript dependencies
	@echo "$(YELLOW)Installing JavaScript dependencies...$(RESET)
	npm install
	@echo "$(GREEN)✓ JavaScript dependencies installed$(RESET)"

install-deps: install-python install-js  ## Install all dependencies

check-env:  ## Check environment configuration
	@echo "$(YELLOW)Checking environment configuration...$(RESET)
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)Warning: .env file not found. Creating from example...$(RESET)"; \
		cp -n .env.example .env; \
	fi
	@echo "$(GREEN)✓ Environment configuration checked$(RESET)"

##@ Run targets
start: start-dev  ## Alias for start-dev

start-dev: check-env  ## Start development server
	@echo "$(YELLOW)Starting development server...$(RESET)"
	@$(POETRY) run uvicorn inceptor.api:app --reload --port $(DEV_PORT)

start-prod: check-env  ## Start production server
	@echo "$(YELLOW)Starting production server on port $(PROD_PORT)...$(RESET)"
	@$(POETRY) run uvicorn inceptor.api:app --host 0.0.0.0 --port $(PROD_PORT)

start-docker:  ## Start using Docker
	@echo "$(YELLOW)Starting with Docker...$(RESET)"
	@$(DOCKER_COMPOSE) up --build

##@ Test
.PHONY: test

test:  ## Run tests
	@echo "$(YELLOW)Running tests...$(RESET)"
	$(POETRY) run pytest $(TEST_PATH) -v

##@ Lint
.PHONY: lint format check

lint:  ## Run linters
	@echo "$(YELLOW)Running linters...$(RESET)"
	$(POETRY) run black --check $(PACKAGE_NAME) $(TEST_PATH)
	$(POETRY) run flake8 $(PACKAGE_NAME) $(TEST_PATH)
	$(POETRY) run mypy $(PACKAGE_NAME) $(TEST_PATH)

format:  ## Format code
	@echo "$(YELLOW)Formatting code...$(RESET)"
	$(POETRY) run black $(PACKAGE_NAME) $(TEST_PATH)
	$(POETRY) run isort $(PACKAGE_NAME) $(TEST_PATH)

check: lint test  ## Run all checks (lint and test)

##@ Build
build:  ## Build package
	@echo "$(YELLOW)Building package...$(RESET)"
	$(POETRY) build
	@echo "$(GREEN)✓ Package built in dist/$(RESET)"

##@ Publish
publish: build  ## Publish package to PyPI
	@echo "$(YELLOW)Publishing to PyPI...$(RESET)"
	$(POETRY) publish

##@ Cleanup
clean:  ## Remove all build, test, coverage and Python artifacts
	@echo "$(YELLOW)Cleaning up...$(RESET)"
	@# Python
	@find . -name '*.pyc' -type f -delete 2>/dev/null || true
	@find . -name '*.pyo' -type f -delete 2>/dev/null || true
	@find . -name '*~' -type f -delete 2>/dev/null || true
	@find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name '.pytest_cache' -type d -exec rm -rf {} + 2>/dev/null || true
	@rm -f .coverage coverage.xml 2>/dev/null || true
	@rm -rf htmlcov/ 2>/dev/null || true
	@# Build artifacts
	@rm -rf build/ dist/ *.egg-info/ 2>/dev/null || true
	@echo "$(GREEN)✓ Clean complete$(RESET)"

clean-all: clean  ## Remove all build, test, coverage and Python artifacts (including virtualenvs)
	@echo "$(YELLOW)Removing virtual environments...$(RESET)"
	@rm -rf $(PYTHON_ENV) .venv/ 2>/dev/null || true

clean-node:  ## Remove node_modules
	@echo "$(YELLOW)Cleaning node modules...$(RESET)"
	@rm -rf $(NODE_MODULES) 2>/dev/null || true
	@rm -f package-lock.json 2>/dev/null || true

clean-docker:  ## Stop and remove Docker containers and volumes
	@echo "$(YELLOW)Cleaning Docker containers and volumes...$(RESET)"
	@if command -v docker-compose >/dev/null 2>&1; then \
		docker-compose down -v --remove-orphans || true; \
	else \
		echo "$(YELLOW)Docker Compose not found, skipping...$(RESET)"; \
	fi

##@ Documentation
docs:  ## Generate documentation
	@echo "$(YELLOW)Generating documentation...$(RESET)"
	@$(POETRY) run mkdocs build
	@echo "$(GREEN)✓ Documentation generated in site/$(RESET)"

serve-docs:  ## Serve documentation locally
	@echo "$(YELLOW)Serving documentation at http://localhost:$(DOCS_PORT)$(RESET)"
	@$(POETRY) run mkdocs serve -a 127.0.0.1:$(DOCS_PORT)

##@ Release
release:  ## Create a new release (bump version, tag, push)
	@echo "$(YELLOW)Creating a new release...$(RESET)"
	@$(POETRY) version $(VERSION)
	git add pyproject.toml
	git commit -m "Bump version to $(shell $(POETRY) version -s)"
	git tag -a v$(shell $(POETRY) version -s) -m "Version $(shell $(POETRY) version -s)"
	git push origin --tags
	@echo "$(GREEN)✓ New release created: v$(shell $(POETRY) version -s)$(RESET)"
	@echo ""
	@echo "Versioning:"
	@echo "  version         - Show current version"
	@echo "  release         - Create a new release"
	@echo "  publish         - Publish new version to all registries"
	@echo "  publish-npm     - Publish to NPM"
	@echo "  publish-pypi    - Publish to PyPI"
	@echo "  publish-docker  - Publish to Docker Hub"
	@echo "Available targets:"
	@echo "  install     Install dependencies"
	@echo "  test       Run tests"
	@echo "  lint       Run linters"
	@echo "  format     Format code"
	@echo "  clean      Clean build artifacts"
	@echo "  build      Build package"
	@echo "  publish    Publish to PyPI"
	@echo "  docs       Generate documentation"
	@echo "  portfolio  Generate portfolio"
	@echo "  git-init   Initialize git repository"

# Environment setup
setup-env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file from .env.example"; \
		echo "Run 'make setup-tokens' to configure your API tokens"; \
	else \
		echo ".env file already exists"; \
		echo "Run 'make setup-tokens' to configure or update your API tokens"; \
	fi

# Setup API tokens for services
setup-tokens:
	@echo "Setting up API tokens for services..."
	@if [ ! -f .env ]; then \
		$(MAKE) setup-env; \
	fi
	@if [ -f "scripts/setup-tokens.sh" ]; then \
		./scripts/setup-tokens.sh; \
	else \
		echo "Error: setup-tokens.sh not found in scripts/"; \
		echo "Please run this from the project root directory"; \
		exit 1; \
	fi

check-env:
	@echo "Checking environment configuration..."
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Run 'make setup-env' first."; \
		exit 1; \
	fi
	@echo "Environment configuration looks good!"

# Install all dependencies
deps: deps-js

# Install JavaScript dependencies
deps-js: check-env
	@echo "Installing Node.js dependencies..."
	@cd $(REACT_APP_DIR) && $(NPM) install --legacy-peer-deps

# Build the project
build: check-env
	@echo "Building project..."
	@cd $(REACT_APP_DIR) && $(NPM) run build
	@echo "Build complete. Files are in $(DIST_DIR)"

# Run the development server
dev: check-env stop-dev
	@echo "Starting development server on port $(DEV_PORT)..."
	@cd $(REACT_APP_DIR) && $(NPM) run dev -- --port $(DEV_PORT) &

# Start the production server
start: check-env stop-prod build
	@echo "Starting production server on port $(PROD_PORT) (http://localhost:$(PROD_PORT))..."
	@if [ -f "$(DIST_DIR)/index.html" ]; then \
		cd $(DIST_DIR) && $(PYTHON) -m http.server $(PROD_PORT) & \
		echo "Production server started at http://localhost:$(PROD_PORT)"; \
	else \
		echo "Error: Build files not found. Run 'make build' first." >&2; \
		exit 1; \
	fi

# Stop all running server processes
stop: stop-dev stop-prod

# Stop development server
stop-dev:
	@echo "Stopping development server..."
	@-pkill -f "vite.*--port $(DEV_PORT)" 2>/dev/null || echo "No development server found on port $(DEV_PORT)"

# Stop production server
stop-prod:
	@echo "Stopping production server..."
	@-pkill -f "python.*http.server $(PROD_PORT)" 2>/dev/null || echo "No production server found on port $(PROD_PORT)"

# Stop all related services (including Docker containers)
stop-all: stop
	@echo "Stopping all related services..."
	@-docker ps -q --filter "name=digitname" | xargs -r docker stop 2>/dev/null || echo "No Docker containers found"

# Show status of running services
status:
	@echo "=== Running Services ==="
	@echo "Development server (port $(DEV_PORT)):"
	@-pgrep -f "vite.*--port $(DEV_PORT)" >/dev/null && echo "  [RUNNING]" || echo "  [STOPPED]"
	@echo "Production server (port $(PROD_PORT)):"
	@-pgrep -f "python.*http.server $(PROD_PORT)" >/dev/null && echo "  [RUNNING]" || echo "  [STOPPED]"
	@echo "Docker containers:"
	@-docker ps --filter "name=digitname" --format "{{.Names}} ({{.Status}})" 2>/dev/null || echo "  No containers found"

# Portfolio Commands
# ========================

# Update portfolio data from all sources
# Portfolio server management
start-portfolio:
	@echo "🚀 Starting portfolio server..."
	@if [ -f $(PORTFOLIO_PID) ]; then \
		echo "Portfolio server is already running"; \
	else \
		cd portfolio && $(PYTHON) serve.py & \
		echo $$! > $(PORTFOLIO_PID); \
		echo "Portfolio server started (check console for URL)"; \
	fi

stop-portfolio:
	@echo "🛑 Stopping portfolio server..."
	@if [ -f $(PORTFOLIO_PID) ]; then \
		kill -9 $$(cat $(PORTFOLIO_PID)) 2>/dev/null || true; \
		rm -f $(PORTFOLIO_PID); \
		echo "Portfolio server stopped"; \
	else \
		echo "No portfolio server is running"; \
	fi

restart-portfolio: stop-portfolio start-portfolio

# Update portfolio data
update-portfolio:
	@echo "🔄 Updating portfolio data..."
	@$(PYTHON) scripts/update_portfolio_repos.py

# Start all services
start: start-portfolio

# Stop all services
stop: stop-portfolio

# Restart all services
restart: restart-portfolio

# Clean up
clean: stop-portfolio
	@echo "🧹 Cleaning up..."
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.py[co]' -delete
	@rm -f $(PORTFOLIO_PID)

# Serve the portfolio using the Python server script
serve-portfolio: update-portfolio
	@echo "🚀 Starting portfolio server..."
	@python scripts/serve_portfolio.py

# ========================
# Development Commands
# ========================

# Run tests
test: check-env
	@echo "Running tests..."
	cd react-app && npm test

# Clean build artifacts
clean: stop
	@echo "Cleaning up..."
	cd react-app && rm -rf node_modules dist
	find . -type d -name 'node_modules' -exec rm -rf {} +

# Show current version
version:
	@echo "Current version: $(shell grep -m 1 "## \[" CHANGELOG.md | grep -o "\[.*\]" | tr -d "[]")"

# Publish to all registries
publish:  publish-pypi

# Publish to PyPI
publish-pypi: check-env build
	@echo "Building package..."
	poetry version patch
	poetry build
	@echo "Publishing to PyPI..."
	@if [ -z "$$PYPI_TOKEN" ]; then \
		echo "Error: PYPI_TOKEN not found in .env file"; \
		echo "Run 'make setup-tokens' to configure your PyPI token"; \
		exit 1; \
	fi
	@echo "Using PyPI token for authentication"
	#@python -m twine upload -u __token__ -p "$$PYPI_TOKEN" dist/*
	poetry publish

# Create a new release
release: version
	@echo "Creating release..."
	@read -p "Enter version number (e.g., 1.0.0): " version; \
	echo "## [$$version] - $(shell date +%Y-%m-%d)" > /tmp/CHANGES; \
	echo "" >> /tmp/CHANGES; \
	echo "### Added" >> /tmp/CHANGES; \
	echo "- " >> /tmp/CHANGES; \
	echo "" >> /tmp/CHANGES; \
	echo "### Changed" >> /tmp/CHANGES; \
	echo "- " >> /tmp/CHANGES; \
	echo "" >> /tmp/CHANGES; \
	echo "### Fixed" >> /tmp/CHANGES; \
	echo "- " >> /tmp/CHANGES; \
	echo "" >> /tmp/CHANGES; \
	${EDITOR:-vi} /tmp/CHANGES; \
	tail -n +2 /tmp/CHANGES | cat - CHANGELOG.md > /tmp/CHANGELOG.md.new && mv /tmp/CHANGELOG.md.new CHANGELOG.md; \
	echo "Changelog updated. Run 'make publish' to publish the new version."



.PHONY: install test lint format clean build publish docs run portfolio

# Project variables
PACKAGE_NAME = digitname
PYTHON = python
PIP = pip
POETRY = poetry

# Default target
all: install

# Install dependencies
install:
	$(POETRY) install

# Run tests
test:
	$(POETRY) run pytest tests/ -v

# Run linters
lint:
	$(POETRY) run black --check $(PACKAGE_NAME) tests
	$(POETRY) run flake8 $(PACKAGE_NAME) tests
	$(POETRY) run mypy $(PACKAGE_NAME) tests

# Format code
format:
	$(POETRY) run black $(PACKAGE_NAME) tests
	$(POETRY) run isort $(PACKAGE_NAME) tests

# Clean build artifacts
clean:
	rm -rf build/ dist/ .mypy_cache/ .pytest_cache/ .coverage htmlcov/ *.egg-info
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.py[co]' -delete 2>/dev/null || true

# Build package
build: clean
	$(POETRY) build

# Publish to PyPI
publish: build
	$(POETRY) publish

# Generate documentation
docs:
	@echo "Generating documentation..."
	@mkdir -p docs
	$(POETRY) run sphinx-apidoc -o docs/source $(PACKAGE_NAME)
	$(POETRY) run sphinx-build -b html docs/source docs/build

# Generate portfolio
portfolio:
	$(POETRY) run python -m $(PACKAGE_NAME).cli generate-portfolio

# Initialize git repository
git-init:
	git init
	git add .
	git commit -m "Initial commit"


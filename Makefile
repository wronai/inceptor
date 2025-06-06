# Port configurations
DEV_PORT := 8003
PROD_PORT := 8001
PORTFOLIO_PORT := 8000
PYTHON := python3
NPM := npm
DOCKER_COMPOSE := docker-compose
DOCKER := docker
PYTHON_ENV := .venv
PYTHON_BIN := $(PYTHON_ENV)/bin/python
PIP := $(PYTHON_ENV)/bin/pip
PYTEST := $(PYTHON_ENV)/bin/pytest
NODE_MODULES := node_modules

# Colors
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

# PID files
PORTFOLIO_PID := /tmp/portfolio_server.pid

# Project directories
REACT_APP_DIR := react-app
DIST_DIR := $(REACT_APP_DIR)/dist

.PHONY: help build run test clean publish version deps deps-js setup-env check-env \
        publish-npm publish-pypi publish-docker update-portfolio setup-tokens \
        start start-dev start-prod stop stop-all status install format lint setup setup-venv \
        install-python install-js install-deps check-env clean clean-pyc clean-node clean-docker

##@ Help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development
setup: setup-venv install-deps check-env  ## Setup development environment

setup-venv:  ## Create Python virtual environment
	@echo "$(YELLOW)Setting up Python virtual environment...$(RESET)"
	$(PYTHON) -m venv $(PYTHON_ENV) || (echo "Failed to create virtual environment. Make sure python3-venv is installed." && exit 1)
	@echo "$(GREEN)✓ Virtual environment created$(RESET)"

install-python:  ## Install Python dependencies
	@echo "$(YELLOW)Installing Python dependencies...$(RESET)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Python dependencies installed$(RESET)"

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
	@$(PYTHON_BIN) server.py $(DEV_PORT)

start-prod: check-env  ## Start production server
	@echo "$(YELLOW)Starting production server on port $(PROD_PORT)...$(RESET)"
	@$(PYTHON_BIN) server.py $(PROD_PORT)

start-docker:  ## Start using Docker
	@echo "$(YELLOW)Starting with Docker...$(RESET)"
	@$(DOCKER_COMPOSE) up --build

##@ Cleanup
clean: clean-pyc clean-node clean-docker  ## Remove all build, test, coverage and Python artifacts

clean-pyc:  ## Remove Python file artifacts
	@echo "$(YELLOW)Cleaning Python cache files...$(RESET)"
	@find . -name '*.pyc' -type f -delete 2>/dev/null || true
	@find . -name '*.pyo' -type f -delete 2>/dev/null || true
	@find . -name '*~' -type f -delete 2>/dev/null || true
	@find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name '.pytest_cache' -type d -exec rm -rf {} + 2>/dev/null || true
	@rm -f .coverage coverage.xml 2>/dev/null || true
	@rm -rf htmlcov/ 2>/dev/null || true

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

##@ Default target
help:
	@echo "Environment Setup:"
	@echo "  setup-env       - Create .env file from example"
	@echo "  setup-tokens    - Interactive setup for API tokens (recommended)"
	@echo "  check-env       - Verify environment configuration"
	@echo ""
	@echo "Development:"
	@echo "  deps            - Install all project dependencies"
	@echo "  deps-js         - Install JavaScript dependencies"
	@echo "  build           - Build the project"
	@echo "  run             - Run the development server"
	@echo "  test            - Run tests"
	@echo "  clean           - Clean build artifacts"
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
publish: publish-npm publish-pypi publish-docker

# Publish to NPM
publish-npm: check-env
	@echo "Publishing to NPM..."
	cd react-app && \
	npm config set //registry.npmjs.org/:_authToken=${NPM_TOKEN} && \
	npm publish --access public

# Publish to PyPI
publish-pypi: check-env build
	@echo "Publishing to PyPI..."
	@if [ -z "$$PYPI_TOKEN" ]; then \
		echo "Error: PYPI_TOKEN not found in .env file"; \
		echo "Run 'make setup-tokens' to configure your PyPI token"; \
		exit 1; \
	fi
	@echo "Using PyPI token for authentication"
	@python -m twine upload -u __token__ -p "$$PYPI_TOKEN" dist/*

# Publish to Docker Hub
publish-docker: check-env
	@echo "Publishing to Docker Hub..."
	@echo "TODO: Add Docker publishing logic"

# Update portfolio data and generate thumbnails/icons
update-portfolio:
	@echo "Updating portfolio data and generating assets..."
	node scripts/update-portfolio.js
	@echo "Portfolio update complete!"

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


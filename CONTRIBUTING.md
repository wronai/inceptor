# Contributing to Inceptor

Thank you for your interest in contributing to Inceptor! We appreciate your time and effort in helping us improve this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#-getting-started)
- [Development Setup](#-development-setup)
- [Making Changes](#-making-changes)
- [Pull Request Process](#-pull-request-process)
- [Code Style](#-code-style)
- [Testing](#-testing)
- [Documentation](#-documentation)
- [Reporting Issues](#-reporting-issues)
- [Feature Requests](#-feature-requests)
- [License](#-license)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 🚀 Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. Create a new **branch** for your changes
4. Make your changes and **commit** them
5. **Push** your changes to your fork
6. Open a **Pull Request**

## 💻 Development Setup

### Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- [Pre-commit](https://pre-commit.com/) for git hooks
- [Ollama](https://ollama.ai/) with Mistral:7b model

### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/inceptor.git
   cd inceptor
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

4. Run tests:
   ```bash
   poetry run pytest
   ```

## ✨ Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/description-of-fix
   ```

2. Make your changes following the code style guidelines

3. Run tests and linters:
   ```bash
   poetry run pre-commit run --all-files
   poetry run pytest
   ```

4. Commit your changes with a descriptive message:
   ```bash
   git commit -m "feat: add new feature"
   # or
   git commit -m "fix: resolve issue with xyz"
   ```

## 🔄 Pull Request Process

1. Ensure your fork is up to date with the main branch
2. Rebase your feature branch on top of the main branch
3. Push your changes to your fork
4. Open a Pull Request with a clear title and description
5. Reference any related issues
6. Ensure all CI checks pass
7. Request reviews from maintainers

## 🎨 Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for all function signatures
- Keep functions small and focused
- Write docstrings for all public functions and classes
- Use meaningful variable and function names

## 🧪 Testing

- Write tests for all new features and bug fixes
- Maintain at least 80% test coverage
- Use descriptive test function names
- Test edge cases and error conditions

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run tests with coverage report
poetry run pytest --cov=inceptor --cov-report=term-missing

# Run a specific test file
poetry run pytest tests/test_module.py
```

## 📚 Documentation

- Update documentation for all new features
- Follow the existing documentation style
- Add examples where helpful
- Ensure all public APIs are documented

### Building Documentation

```bash
# Install documentation dependencies
poetry install --with docs

# Build documentation
poetry run mkdocs build

# Serve documentation locally
poetry run mkdocs serve
```

## 🐛 Reporting Issues

When reporting issues, please include:

1. A clear, descriptive title
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Environment details (OS, Python version, etc.)
6. Any relevant error messages or logs

## 💡 Feature Requests

We welcome feature requests! Please:

1. Check if a similar feature already exists
2. Explain why this feature would be valuable
3. Provide examples of how it would be used
4. Consider contributing a pull request

## 📄 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

## 🙏 Thank You!

Your contributions help make Inceptor better for everyone. Thank you for being part of our community!

# 🌀 Inceptor

**AI-Powered Multi-Level Solution Architecture Generator**

> **Note**: This project has been refactored for better maintainability and organization. The core functionality remains the same, but the code is now more modular and easier to extend.

[![PyPI Version](https://img.shields.io/pypi/v/inceptor?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/inceptor/)
[![Python Version](https://img.shields.io/pypi/pyversions/inceptor?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/wronai/inceptor?color=blue)](https://github.com/wronai/inceptor/blob/main/LICENSE)
[![Documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat&logo=read-the-docs)](https://wronai.github.io/inceptor/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/wronai/inceptor/gh-pages.yml?branch=main&label=docs%20build)](https://github.com/wronai/inceptor/actions/workflows/gh-pages.yml)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/imports-isort-ef8336.svg)](https://pycqa.github.io/isort/)
[![Type Checker: mypy](https://img.shields.io/badge/type%20checker-mypy-blue.svg)](http://mypy-lang.org/)
[![Linter: flake8](https://img.shields.io/badge/linter-flake8-3776ab.svg)](https://flake8.pycqa.org/)

Inceptor is a powerful AI-powered tool that helps you design, generate, and implement complex software architectures using natural language. Built with Ollama's Mistral:7b model, it creates multi-level architecture designs that evolve from high-level concepts to detailed implementation plans.

## ✨ Key Features

- **🤖 AI-Powered**: Leverages Ollama's Mistral:7b for intelligent architecture generation
- **🏗️ Multi-Level Design**: Creates 5 distinct architecture levels (LIMBO → DREAM → REALITY → DEEPER → DEEPEST)
- **🔍 Context-Aware**: Understands requirements from natural language descriptions
- **💻 Interactive CLI**: Command-line interface with autocomplete and suggestions
- **📊 Structured Output**: Exports to Markdown, JSON, YAML, and more
- **🚀 Zero-Setup**: Works out of the box with local Ollama installation
- **🔌 Extensible**: Plugin system for custom generators and templates

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) with Mistral:7b model
- 4GB RAM (minimum)

### Installation

```bash
# Install from PyPI
pip install inceptor

# Or install from source
git clone https://github.com/wronai/inceptor.git
cd inceptor
make install  # Installs in development mode with all dependencies

# Start Ollama server (if not already running)
ollama serve
```

### Basic Usage

```bash
# Generate architecture from a description
inceptor "I need a REST API for a todo app with user authentication"

# Start interactive shell
inceptor shell
```

### Using the Python API

```python
from inceptor import DreamArchitect, Solution, ArchitectureLevel

# Create an architect instance
architect = DreamArchitect()

# Generate a solution
problem = """
I need a task management system for a small development team.
The team consists of 5 people and uses Python, FastAPI, and PostgreSQL.
The system should have a web interface and REST API.
"""

# Generate solution with 3 levels of detail
solution = architect.inception(problem, max_levels=3)

# Access solution components
print(f"Problem: {solution.problem}")
print(f"Components: {len(solution.architecture.get('limbo', {}).get('components', []))}")
print(f"Tasks: {len(solution.tasks)}")

# Save to JSON
import json
from dataclasses import asdict, is_dataclass

def convert_dataclass(obj):
    if is_dataclass(obj):
        return {k: convert_dataclass(v) for k, v in asdict(obj).items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_dataclass(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: convert_dataclass(v) for k, v in obj.items()}
    elif hasattr(obj, 'name'):  # For Enums
        return obj.name
    return obj

with open("solution.json", "w") as f:
    json.dump(convert_dataclass(solution), f, indent=2, ensure_ascii=False)
```

## 🏗️ Project Structure

After refactoring, the project has a cleaner, more modular structure:

```
src/inceptor/
├── __init__.py           # Package exports and version
├── inceptor.py           # Compatibility layer
└── core/                 # Core functionality
    ├── __init__.py       # Core package exports
    ├── enums.py          # ArchitectureLevel enum
    ├── models.py         # Solution and Task dataclasses
    ├── context_extractor.py # Context extraction utilities
    ├── ollama_client.py  # Ollama API client
    ├── prompt_templates.py # Prompt templates for each level
    ├── dream_architect.py # Main architecture generation logic
    └── utils.py          # Utility functions
```

## 🏗️ Multi-Level Architecture

Inceptor structures architectures across 5 levels of detail:

| Level | Name | Description | Output |
|-------|------|-------------|--------|
| 1 | LIMBO | Problem analysis & decomposition | High-level components |
| 2 | DREAM | Component design & interactions | API contracts, Data flows |
| 3 | REALITY | Implementation details | Code structure, Tech stack |
| 4 | DEEPER | Integration & deployment | CI/CD, Infrastructure |
| 5 | DEEPEST | Optimization & scaling | Performance, Monitoring |

## 🛠️ Development

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/wronai/inceptor.git
   cd inceptor
   ```

2. Set up the development environment:
   ```bash
   # Install Python dependencies
   make install
   
   # Install pre-commit hooks
   pre-commit install
   
   # Start Ollama server (in a separate terminal)
   ollama serve
   ```

### Common Tasks

```bash
# Install development dependencies
make install

# Run tests
make test

# Run tests with coverage
make test-cov

# Check code style
make lint

# Format code
make format

# Build documentation
make docs

# Run documentation server (http://localhost:8001)
make serve-docs

# Build package
make build

# Clean up
make clean

# Run a local example
python -m src.inceptor.inceptor
```

## 📚 Documentation

For full documentation, please visit [https://wronai.github.io/inceptor/](https://wronai.github.io/inceptor/)

- [Installation Guide](https://wronai.github.io/inceptor/installation/)
- [Quick Start](https://wronai.github.io/inceptor/quick-start/)
- [User Guide](https://wronai.github.io/inceptor/guide/)
- [API Reference](https://wronai.github.io/inceptor/api/)
- [Examples](https://wronai.github.io/inceptor/examples/)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) to get started.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for the powerful AI models
- [Mistral AI](https://mistral.ai/) for the 7B model
- The open-source community for invaluable tools and libraries

```bash
# 1. Zainstaluj MkDocs
pip install mkdocs-material mkdocstrings[python] mkdocs-awesome-pages-plugin

# 2. Stwórz strukturę docs/
mkdir -p docs/{guide,architecture,api,development,examples,about,assets/{css,js,images}}

# 3. Uruchom development server
mkdocs serve

# 4. Build i deploy
mkdocs build
mkdocs gh-deploy  # GitHub Pages
```

## 📚 **Struktura dokumentacji:**

- **Home**: Installation, Quick Start, Features
- **User Guide**: Getting Started, CLI Reference, Examples  
- **Architecture**: Multi-Level Design, Prompts, Ollama Integration
- **API Reference**: Auto-generated z kodu
- **Development**: Contributing, Testing, Release Process
- **Examples**: Real-world use cases, troubleshooting

## 🎨 **Customizacja:**

- **Theme**: Material Design z custom colors
- **Logo**: Inception-inspired rotating animation
- **Terminal**: Code examples z animacją
- **Social**: GitHub, PyPI, Docker links

## 🔧 **Plugin features:**

- **Search**: Zaawansowane z język separatorami
- **Git dates**: Automatic creation/modification dates
- **Minify**: Optimized HTML/CSS/JS
- **Privacy**: GDPR-compliant
- **Tags**: Content categorization

Teraz wystarczy dodać treść do folderów w `docs/` i masz profesjonalną dokumentację gotową na deployment! 🎯

**Przykładowa komenda uruchomienia:**
```bash
mkdocs serve  # http://localhost:8000
```
# 🌀 Inceptor

**AI-Powered Multi-Level Solution Architecture Generator**

[![PyPI version](https://img.shields.io/pypi/v/inceptor)](https://pypi.org/project/inceptor/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/wronai/inceptor/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://wronai.github.io/inceptor/)
[![Tests](https://github.com/wronai/inceptor/actions/workflows/tests.yml/badge.svg)](https://github.com/wronai/inceptor/actions/workflows/tests.yml)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
from inceptor import Architect

# Create an architect instance
architect = Architect()

# Generate a solution
solution = architect.generate(
    "E-commerce platform with microservices",
    context={
        "cloud_provider": "aws",
        "container_orchestrator": "kubernetes",
        "monitoring": ["prometheus", "grafana"],
        "budget": "medium"
    },
    levels=4
)

# Export to different formats
print(solution.to_markdown())  # Markdown
print(solution.to_json())      # JSON
print(solution.to_yaml())      # YAML
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
   make install
   ```

### Common Tasks

```bash
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

# Run documentation server
make serve-docs

# Build package
make build

# Clean up
make clean
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
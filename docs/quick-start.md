# 🚀 Quick Start Guide

This guide will help you get started with Inceptor in just a few minutes.

## Prerequisites

- Ollama with Mistral:7b model installed (see [Installation Guide](installation.md))
- Python 3.8 or higher
- Basic familiarity with command line

## Your First Architecture

1. **Start with a simple command**:
   ```bash
   inceptor "I need a REST API for a todo app with user authentication"
   ```

2. **Interactive Mode**:
   ```bash
   inceptor shell
   ```
   Then type your requirements in the interactive prompt.

## Basic Commands

### Generate Architecture
```bash
# Basic usage
inceptor "Your architecture requirements here"

# Specify output format (default: markdown)
inceptor --format json "Your requirements"

# Save output to a file
inceptor "Your requirements" > architecture.md
```

### Interactive Shell
```bash
# Start interactive shell
inceptor shell

# In the shell:
> help                 # Show available commands
> clear               # Clear screen
> exit                # Exit the shell
```

## Example Workflow

1. **Define your requirements**:
   ```bash
   inceptor "I need a microservices architecture for an e-commerce platform with:
   - Product catalog
   - User authentication
   - Shopping cart
   - Payment processing
   - Order management"
   ```

2. **Review the generated architecture**

3. **Refine and iterate**:
   ```bash
   inceptor "Add Redis caching to the previous architecture"
   ```

## Next Steps

- Learn about [Configuration Options](guide/configuration.md)
- Explore [Advanced Features](guide/advanced-features.md)
- Check out [Examples](examples/)
- Read the [CLI Reference](guide/cli-reference.md)

## Getting Help

- Run `inceptor --help` for command-line options
- Check the [FAQ](about/faq.md) for common questions
- [Open an issue](https://github.com/yourusername/inceptor/issues) for bugs or feature requests

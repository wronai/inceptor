# 📦 Installation Guide

## System Requirements

- Python 3.8 or higher
- Ollama with Mistral:7b model
- 4GB RAM (minimum)
- Internet connection (for initial model download)
- 10GB free disk space (for models and dependencies)

## Installing Ollama

### macOS/Linux
```bash
# Download and install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Download the Mistral:7b model
ollama pull mistral:7b
```

### Windows
1. Download the installer from [Ollama's website](https://ollama.ai/download)
2. Run the installer
3. Open a new command prompt and run:
   ```cmd
   ollama pull mistral:7b
   ```

## Installing Inceptor

### Using pip (Recommended)
```bash
pip install inceptor
```

### From Source
```bash
# Clone the repository
git clone https://github.com/yourusername/inceptor.git
cd inceptor

# Install in development mode
pip install -e .
```

### Development Setup
For contributing to Inceptor:
```bash
git clone https://github.com/yourusername/inceptor.git
cd inceptor

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Verifying Installation

```bash
# Check Ollama is running
ollama list

# Check Inceptor installation
inceptor --version

# Check system status
inceptor status
```

## Troubleshooting

### Common Issues

1. **Ollama not found**
   - Ensure Ollama is properly installed and in your system PATH
   - Try restarting your terminal or computer

2. **Model not found**
   - Verify you've pulled the correct model: `ollama pull mistral:7b`
   - Check your internet connection

3. **Permission errors**
   - On Linux/macOS, you might need to use `sudo` for Ollama commands
   - Consider adding your user to the `docker` group if using Docker

## Next Steps

- [Quick Start Guide](quick-start.md)
- [Configuration Options](guide/configuration.md)
- [CLI Reference](guide/cli-reference.md)

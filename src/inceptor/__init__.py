"""Inceptor - AI-Powered Multi-Level Solution Architecture Generator

This package provides tools for generating and managing multi-level solution architectures
using AI-powered analysis and generation capabilities.
"""

__version__ = "0.1.0"
__author__ = "Tom Sapletta"

# Import main components
from .cli import cli, generate, shell  # noqa: F401

# Core functionality
from .core import (
    DreamArchitect,
    OllamaClient,
    ContextExtractor,
    PromptTemplates,
    Solution,
    Task,
    ArchitectureLevel,
    quick_solution,
    analyze_context
)

__all__ = [
    'cli',
    'generate',
    'shell',
    'DreamArchitect',
    'OllamaClient',
    'ContextExtractor',
    'PromptTemplates',
    'Solution',
    'Task',
    'ArchitectureLevel',
    'quick_solution',
    'analyze_context'
]
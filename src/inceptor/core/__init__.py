"""
Core module for the Inceptor architecture generation system.

This module contains the main components for generating multi-level solution architectures.
"""

from .dream_architect import DreamArchitect
from .ollama_client import OllamaClient
from .context_extractor import ContextExtractor
from .prompt_templates import PromptTemplates
from .models import Solution, Task
from .enums import ArchitectureLevel
from .utils import quick_solution, analyze_context

__all__ = [
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

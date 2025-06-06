"""
DreamArchitect - Multi-Level Solution Architecture Generator
Współpraca z Ollama Mistral:7b dla generowania architektur rozwiązań

This is a compatibility layer that imports all functionality from the new modular structure.
For new code, consider importing directly from inceptor.core modules.

Installation:
pip install ollama requests pydantic
"""

# Import everything from the core module
from .core import (
    # Main classes
    DreamArchitect,
    OllamaClient,
    ContextExtractor,
    PromptTemplates,
    
    # Models
    Solution,
    Task,
    ArchitectureLevel,
    
    # Utility functions
    quick_solution,
    analyze_context
)

# For backward compatibility
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

# Example usage
if __name__ == "__main__":
    # Example usage
    architect = DreamArchitect()
    
    problem = """
    I need a task management system for a small development team.
    The team consists of 5 people and uses Python, FastAPI, and PostgreSQL.
    The system should have a web interface and REST API.
    """
    
    print("Generating solution...")
    solution = architect.inception(problem, max_levels=3)
    
    print("\nGenerated Solution:")
    print(f"Problem: {solution.problem}")
    print(f"Components: {len(solution.architecture.get('limbo', {}).get('components', []))}")
    print(f"Tasks: {len(solution.tasks)}")
    
    # Save to file
    with open("solution.json", "w") as f:
        from dataclasses import asdict, is_dataclass
        import json
        
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
            
        json.dump(convert_dataclass(solution), f, indent=2, ensure_ascii=False)
    
    print("\nSolution saved to solution.json")

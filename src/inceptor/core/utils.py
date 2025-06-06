from typing import Dict, Any
from .dream_architect import DreamArchitect
from .context_extractor import ContextExtractor
from .models import Solution

def quick_solution(problem: str, levels: int = 3) -> Solution:
    """Generate a quick solution with default settings.
    
    Args:
        problem: Problem description
        levels: Number of architecture levels (3-5)
        
    Returns:
        Solution object
    """
    architect = DreamArchitect()
    return architect.inception(problem, max_levels=levels)

def analyze_context(text: str) -> Dict[str, Any]:
    """Analyze context from text.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with extracted context
    """
    extractor = ContextExtractor()
    return extractor.extract_context(text)

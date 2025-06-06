from dataclasses import dataclass
from typing import Dict, Any, List
from .enums import ArchitectureLevel

@dataclass
class Task:
    """Represents a task in the architecture generation process."""
    id: str
    level: ArchitectureLevel
    description: str
    context: Dict[str, Any]
    dependencies: List[str]
    output_format: str
    success_criteria: List[str]

@dataclass
class Solution:
    """Represents a complete solution with all its components."""
    problem: str
    architecture: Dict[str, Any]
    tasks: List[Task]
    implementation: Dict[str, str]
    metadata: Dict[str, Any]

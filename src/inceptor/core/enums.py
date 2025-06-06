from enum import Enum

class ArchitectureLevel(Enum):
    """Represents different levels of architecture abstraction."""
    LIMBO = 1  # Meta-Architecture (Business Problem → Components)
    DREAM = 2  # Solution Design (Components → Technical Specs)
    REALITY = 3  # Implementation (Specs → Code/Config)
    DEEPER = 4  # Integration (Code → Deployment/Monitoring)
    DEEPEST = 5  # Evolution (Deployment → Optimization/Scaling)

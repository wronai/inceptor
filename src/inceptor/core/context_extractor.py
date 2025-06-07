import re
from typing import Dict, Any, List

class ContextExtractor:
    """Extracts context from various sources using predefined patterns."""

    CONTEXT_PATTERNS = {
        'technology': [
            r'\b(python|javascript|react|flask|fastapi|django|nodejs|typescript)\b',
            r'\b(docker|kubernetes|aws|azure|gcp|terraform)\b',
            r'\b(mysql|postgresql|mongodb|redis|elasticsearch)\b'
        ],
        'problem_type': [
            r'\b(logging|monitoring|security|performance|testing|deployment)\b',
            r'\b(authentication|authorization|api|frontend|backend|database)\b',
            r'\b(ci/cd|devops|automation|scaling|optimization)\b'
        ],
        'scale': [
            r'\b(small|medium|large|enterprise|startup|team|personal)\b',
            r'\b(\d+\s*users?|\d+\s*requests?|\d+\s*servers?)\b'
        ],
        'urgency': [
            r'\b(urgent|asap|quick|fast|immediate|prototype|poc)\b',
            r'\b(production|critical|important|nice to have)\b'
        ],
        'constraints': [
            r'\b(budget|time|resources|team size|deadline)\b',
            r'\b(security|compliance|gdpr|hipaa|pci)\b',
            r'\b(legacy|existing|migration|greenfield)\b'
        ]
    }

    @staticmethod
    def extract_context(text: str) -> Dict[str, List[str]]:
        """Extracts context from text using regex patterns.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing extracted context categories and matches
        """
        context = {}

        for category, patterns in ContextExtractor.CONTEXT_PATTERNS.items():
            matches = []
            for pattern in patterns:
                matches.extend(re.findall(pattern, text.lower()))
            context[category] = list(set(matches))

        return context

    @staticmethod
    def enrich_context(context: Dict[str, Any], additional_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Enriches context with additional information and sets defaults.
        
        Args:
            context: Existing context dictionary
            additional_info: Additional context information to add
            
        Returns:
            Enriched context dictionary
        """
        if additional_info:
            context.update(additional_info)

        # Add intelligent defaults
        if not context.get('scale'):
            context['scale'] = ['medium']

        if not context.get('urgency'):
            context['urgency'] = ['normal']

        return context

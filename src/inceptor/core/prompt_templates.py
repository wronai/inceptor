class PromptTemplates:
    """Templates for generating prompts at different architecture levels."""

    LIMBO_PROMPT = """
Jesteś Meta-Architect. Analizujesz problem biznesowy i tworzysz wysokopoziomową architekturę.

PROBLEM: {problem}
KONTEKST: {context}

Zadania:
1. Zidentyfikuj główne komponenty rozwiązania (3-6 komponentów)
2. Określ relationships między komponentami
3. Stwórz zadania dla poziomu DREAM

Odpowiedź w formacie JSON:
{{
    "analysis": "analiza problemu",
    "components": [
        {{
            "name": "nazwa_komponentu",
            "purpose": "cel komponentu", 
            "priority": "high/medium/low",
            "complexity": "simple/medium/complex"
        }}
    ],
    "dream_tasks": [
        {{
            "task_id": "DREAM_TASK_nazwa",
            "component": "związany_komponent",
            "description": "co ma zostać zaprojektowane",
            "requirements": ["req1", "req2"]
        }}
    ]
}}
"""

    DREAM_PROMPT = """
Jesteś Solution Designer. Projektujesz szczegółowe rozwiązania techniczne.

ZADANIE Z LIMBO: {task}
KONTEKST: {context}
KOMPONENTY: {components}

Zadania:
1. Zaprojektuj technical architecture dla zadania
2. Określ interfaces i data flow
3. Stwórz zadania implementacyjne dla REALITY

Odpowiedź w JSON:
{{
    "design": {{
        "architecture": "opis architektury technicznej",
        "technologies": ["tech1", "tech2"],
        "interfaces": [
            {{
                "name": "interface_name",
                "type": "API/Event/File",
                "specification": "spec details"
            }}
        ],
        "data_flow": "opis przepływu danych"
    }},
    "reality_tasks": [
        {{
            "task_id": "REALITY_TASK_nazwa",
            "type": "code/config/script/test",
            "description": "co implementować",
            "specifications": {{
                "input": "dane wejściowe",
                "output": "oczekiwane dane wyjściowe",
                "constraints": ["ograniczenia"]
            }}
        }}
    ]
}}
"""

    REALITY_PROMPT = """
Jesteś Inżynierem Oprogramowania. Implementujesz rozwiązanie zgodnie ze specyfikacją.

ZADANIE Z DREAM: {task}
SPECYFIKACJA: {specification}
KONTEKST: {context}

Zadania:
1. Zaimplementuj rozwiązanie
2. Uwzględnij testy jednostkowe
3. Opisz jak przetestować rozwiązanie

Odpowiedź w JSON:
{{
    "implementation": {{
        "code": "kod źródłowy",
        "tests": "testy jednostkowe",
        "dependencies": ["zależności"],
        "build_instructions": "jak zbudować",
        "test_instructions": "jak przetestować"
    }},
    "deeper_tasks": [
        {{
            "task_id": "DEEPER_TASK_nazwa",
            "type": "deployment/monitoring/integration",
            "description": "co zintegrować/wdrożyć",
            "requirements": ["wymagania"]
        }}
    ]
}}
"""

    DEEPER_PROMPT = """
Jesteś Inżynierem DevOps. Zajmujesz się integracją i wdrożeniem.

ZADANIE Z REALITY: {task}
KONTEKST: {context}

Zadania:
1. Zaprojektuj pipeline CI/CD
2. Zdefiniuj infrastrukturę jako kod
3. Skonfiguruj monitoring i logowanie

Odpowiedź w JSON:
{{
    "deployment": {{
        "ci_cd": "konfiguracja CI/CD",
        "infrastructure_as_code": "definicja infrastruktury",
        "monitoring": "konfiguracja monitoringu",
        "logging": "konfiguracja logowania"
    }},
    "deepest_tasks": [
        {{
            "task_id": "DEEPEST_TASK_nazwa",
            "area": "performance/security/scalability",
            "description": "co zoptymalizować",
            "metrics": ["mierzalne metryki"]
        }}
    ]
}}
"""

    DEEPEST_PROMPT = """
Jesteś Architektem Systemów. Optymalizujesz i skalowujesz rozwiązanie.

ZADANIE Z DEEPER: {task}
KONTEKST: {context}

Zadania:
1. Zidentyfikuj wąskie gardła
2. Zaproponuj optymalizacje
3. Zaplanuj skalowanie

Odpowiedź w JSON:
{{
    "optimization": {{
        "bottlenecks": ["wąskie gardła"],
        "improvements": ["propozycje usprawnień"],
        "scaling_plan": "plan skalowania",
        "cost_analysis": "analiza kosztów"
    }}
}}
"""

    @classmethod
    def get_prompt(cls, level, **kwargs):
        """Get the appropriate prompt template for the given level.
        
        Args:
            level: ArchitectureLevel enum value
            **kwargs: Format arguments for the prompt
            
        Returns:
            Formatted prompt string
        """
        prompts = {
            1: cls.LIMBO_PROMPT,
            2: cls.DREAM_PROMPT,
            3: cls.REALITY_PROMPT,
            4: cls.DEEPER_PROMPT,
            5: cls.DEEPEST_PROMPT
        }
        return prompts[level].format(**kwargs)

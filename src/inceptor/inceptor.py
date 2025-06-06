"""
DreamArchitect - Multi-Level Solution Architecture Generator
Współpraca z Ollama Mistral:7b dla generowania architektur rozwiązań

Installation:
pip install ollama requests pydantic
"""

import json
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import requests
from pydantic import BaseModel


class ArchitectureLevel(Enum):
    LIMBO = 1  # Meta-Architecture (Business Problem → Components)
    DREAM = 2  # Solution Design (Components → Technical Specs)
    REALITY = 3  # Implementation (Specs → Code/Config)
    DEEPER = 4  # Integration (Code → Deployment/Monitoring)
    DEEPEST = 5  # Evolution (Deployment → Optimization/Scaling)


@dataclass
class Task:
    id: str
    level: ArchitectureLevel
    description: str
    context: Dict[str, Any]
    dependencies: List[str]
    output_format: str
    success_criteria: List[str]


@dataclass
class Solution:
    problem: str
    architecture: Dict[str, Any]
    tasks: List[Task]
    implementation: Dict[str, str]
    metadata: Dict[str, Any]


class ContextExtractor:
    """Wyciąga kontekst z różnych źródeł"""

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
        """Wyciąga kontekst z tekstu używając regex patterns"""
        context = {}

        for category, patterns in ContextExtractor.CONTEXT_PATTERNS.items():
            matches = []
            for pattern in patterns:
                matches.extend(re.findall(pattern, text.lower()))
            context[category] = list(set(matches))

        return context

    @staticmethod
    def enrich_context(context: Dict, additional_info: Dict = None) -> Dict:
        """Wzbogaca kontekst o dodatkowe informacje"""
        if additional_info:
            context.update(additional_info)

        # Dodaj intelligent defaults
        if not context.get('scale'):
            context['scale'] = ['medium']

        if not context.get('urgency'):
            context['urgency'] = ['normal']

        return context


class OllamaClient:
    """Klient do komunikacji z Ollama Mistral:7b"""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "mistral:7b"

    def generate(self, prompt: str, system_prompt: str = "", max_tokens: int = 2000) -> str:
        """Generuje odpowiedź z Ollama"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "system": system_prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.7
                    }
                }
            )
            response.raise_for_status()
            return response.json()['response']
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")


class PromptTemplates:
    """Szablony promptów dla różnych poziomów architektury"""

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
                "input": "input format",
                "output": "output format", 
                "dependencies": ["dep1", "dep2"]
            }}
        }}
    ]
}}
"""

    REALITY_PROMPT = """
Jesteś Code Generator. Tworzysz konkretne implementacje.

ZADANIE Z DREAM: {task}
SPECS: {specifications}
KONTEKST: {context}

Stwórz gotową implementację:
- Kompletny kod bez placeholderów
- Configuration files
- Documentation
- Tests (jeśli wymagane)

Odpowiedź w JSON:
{{
    "implementation": {{
        "files": [
            {{
                "path": "ścieżka/do/pliku",
                "content": "pełna zawartość pliku",
                "description": "opis pliku"
            }}
        ],
        "commands": ["komenda1", "komenda2"],
        "documentation": "instrukcje użycia"
    }}
}}
"""

    DEEPER_PROMPT = """
Jesteś Integration Specialist. Łączysz implementacje w działający system.

IMPLEMENTACJE: {implementations}
KONTEKST: {context}

Stwórz deployment i monitoring:
- Docker/Kubernetes configs
- CI/CD pipelines  
- Monitoring setup
- Integration tests

JSON format podobny do REALITY.
"""

    DEEPEST_PROMPT = """
Jesteś Optimization Expert. Skaling i ewolucja systemu.

SYSTEM: {system}
METRICS: {metrics}
KONTEKST: {context}

Zaproponuj:
- Performance optimizations
- Scaling strategies
- Monitoring improvements
- Future roadmap

JSON z recommendations i migration plans.
"""


class DreamArchitect:
    """Główna klasa biblioteki"""

    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama = OllamaClient(ollama_url)
        self.context_extractor = ContextExtractor()

    def inception(self, problem: str, max_levels: int = 3, additional_context: Dict = None) -> Solution:
        """
        Główna metoda - tworzy wielopoziomową architekturę

        Args:
            problem: Opis problemu jednym zdaniem lub więcej
            max_levels: Maksymalna głębokość (3-5)
            additional_context: Dodatkowy kontekst

        Returns:
            Solution object z kompletną architekturą
        """

        # Wyciągnij kontekst
        context = self.context_extractor.extract_context(problem)
        context = self.context_extractor.enrich_context(context, additional_context)

        solution = Solution(
            problem=problem,
            architecture={},
            tasks=[],
            implementation={},
            metadata={"levels": max_levels, "context": context}
        )

        try:
            # Level 1: LIMBO - Meta Architecture
            limbo_result = self._execute_limbo(problem, context)
            solution.architecture['limbo'] = limbo_result

            if max_levels >= 2:
                # Level 2: DREAM - Solution Design
                dream_results = self._execute_dream(limbo_result, context)
                solution.architecture['dream'] = dream_results

                if max_levels >= 3:
                    # Level 3: REALITY - Implementation
                    reality_results = self._execute_reality(dream_results, context)
                    solution.implementation = reality_results

                    if max_levels >= 4:
                        # Level 4: DEEPER - Integration
                        deeper_results = self._execute_deeper(reality_results, context)
                        solution.architecture['deeper'] = deeper_results

                        if max_levels >= 5:
                            # Level 5: DEEPEST - Optimization
                            deepest_results = self._execute_deepest(solution, context)
                            solution.architecture['deepest'] = deepest_results

        except Exception as e:
            solution.metadata['error'] = str(e)

        return solution

    def _execute_limbo(self, problem: str, context: Dict) -> Dict:
        """Wykonuje Level 1 - Meta Architecture"""
        prompt = PromptTemplates.LIMBO_PROMPT.format(
            problem=problem,
            context=json.dumps(context, indent=2)
        )

        response = self.ollama.generate(prompt)
        return self._parse_json_response(response)

    def _execute_dream(self, limbo_result: Dict, context: Dict) -> Dict:
        """Wykonuje Level 2 - Solution Design"""
        dream_results = {}

        for task in limbo_result.get('dream_tasks', []):
            prompt = PromptTemplates.DREAM_PROMPT.format(
                task=json.dumps(task, indent=2),
                context=json.dumps(context, indent=2),
                components=json.dumps(limbo_result.get('components', []), indent=2)
            )

            response = self.ollama.generate(prompt)
            dream_results[task['task_id']] = self._parse_json_response(response)

        return dream_results

    def _execute_reality(self, dream_results: Dict, context: Dict) -> Dict:
        """Wykonuje Level 3 - Implementation"""
        reality_results = {}

        for dream_task_id, dream_data in dream_results.items():
            for task in dream_data.get('reality_tasks', []):
                prompt = PromptTemplates.REALITY_PROMPT.format(
                    task=json.dumps(task, indent=2),
                    specifications=json.dumps(task.get('specifications', {}), indent=2),
                    context=json.dumps(context, indent=2)
                )

                response = self.ollama.generate(prompt)
                reality_results[task['task_id']] = self._parse_json_response(response)

        return reality_results

    def _execute_deeper(self, reality_results: Dict, context: Dict) -> Dict:
        """Wykonuje Level 4 - Integration"""
        prompt = PromptTemplates.DEEPER_PROMPT.format(
            implementations=json.dumps(reality_results, indent=2),
            context=json.dumps(context, indent=2)
        )

        response = self.ollama.generate(prompt)
        return self._parse_json_response(response)

    def _execute_deepest(self, solution: Solution, context: Dict) -> Dict:
        """Wykonuje Level 5 - Optimization"""
        prompt = PromptTemplates.DEEPEST_PROMPT.format(
            system=json.dumps(solution.architecture, indent=2),
            metrics={},  # TODO: Implement metrics collection
            context=json.dumps(context, indent=2)
        )

        response = self.ollama.generate(prompt)
        return self._parse_json_response(response)

    def _parse_json_response(self, response: str) -> Dict:
        """Parsuje odpowiedź JSON z Ollama"""
        try:
            # Usuń markdown formatting jeśli istnieje
            response = re.sub(r'```json\s*\n?', '', response)
            response = re.sub(r'\n?```', '', response)
            return json.loads(response)
        except json.JSONDecodeError as e:
            # Fallback - spróbuj wyciągnąć JSON z tekstu
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    pass
            return {"error": f"Cannot parse JSON: {str(e)}", "raw_response": response}


# Utility functions
def quick_solution(problem: str, levels: int = 3) -> Dict:
    """Szybka funkcja dla prostego użycia"""
    architect = DreamArchitect()
    solution = architect.inception(problem, max_levels=levels)
    return asdict(solution)


def analyze_context(text: str) -> Dict:
    """Analizuje kontekst z tekstu"""
    return ContextExtractor.extract_context(text)


# Example usage
if __name__ == "__main__":
    # Przykład użycia
    architect = DreamArchitect()

    # Test 1: Simple logging system
    solution1 = architect.inception(
        "Potrzebuję system logowania dla aplikacji Python Flask + React frontend",
        max_levels=3
    )

    # Test 2: Complex system with context
    solution2 = architect.inception(
        "Stwórz CI/CD pipeline z automatycznym testowaniem i deployment do AWS dla team 5 osób",
        max_levels=4,
        additional_context={
            "budget": "medium",
            "team_experience": "intermediate",
            "timeline": "2 weeks"
        }
    )

    print("Solution 1:", json.dumps(asdict(solution1), indent=2))
    print("\n" + "=" * 50 + "\n")
    print("Solution 2:", json.dumps(asdict(solution2), indent=2))
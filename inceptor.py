#!/usr/bin/env python3
"""
Najprostszy Dream Architect System
Minimal implementation z Ollama integration
"""

import json
import requests
from typing import Dict, List


class SimpleDreamArchitect:
    """Minimalny Dream Architect - 3 poziomy: LIMBO → DREAM → REALITY"""

    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.model = "mistral:7b"

    def ask_ollama(self, prompt: str) -> str:
        """Wysyła prompt do Ollama i zwraca odpowiedź"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.7}
                }
            )
            return response.json()['response']
        except Exception as e:
            return f"ERROR: {str(e)}"

    def limbo(self, problem: str) -> Dict:
        """LEVEL 1: Meta-Architecture - problem → komponenty"""
        prompt = f"""
        Problem: {problem}

        Analizuj problem i podaj odpowiedź w JSON:
        {{
            "components": ["komponent1", "komponent2", "komponent3"],
            "tasks": [
                {{
                    "name": "task1",
                    "description": "co zrobić"
                }}
            ]
        }}
        """

        response = self.ask_ollama(prompt)
        try:
            # Wyciągnij JSON z odpowiedzi
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(response[start:end])
        except:
            pass

        # Fallback jeśli JSON nie parsuje
        return {
            "components": ["frontend", "backend", "database"],
            "tasks": [{"name": "design", "description": f"Zaprojektuj rozwiązanie dla: {problem}"}]
        }

    def dream(self, limbo_result: Dict) -> Dict:
        """LEVEL 2: Solution Design - komponenty → technical specs"""
        components = limbo_result.get('components', [])

        prompt = f"""
        Komponenty: {components}

        Zaprojektuj technical solution w JSON:
        {{
            "architecture": "opis architektury",
            "technologies": ["tech1", "tech2"],
            "implementation_tasks": [
                {{
                    "file": "nazwa_pliku",
                    "description": "co implementować"
                }}
            ]
        }}
        """

        response = self.ask_ollama(prompt)
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(response[start:end])
        except:
            pass

        return {
            "architecture": f"System wykorzystujący {', '.join(components)}",
            "technologies": ["Python", "JavaScript"],
            "implementation_tasks": [
                {"file": "main.py", "description": "Główna implementacja"},
                {"file": "config.yml", "description": "Konfiguracja"}
            ]
        }

    def reality(self, dream_result: Dict) -> Dict:
        """LEVEL 3: Implementation - specs → kod"""
        tasks = dream_result.get('implementation_tasks', [])
        files = {}

        for task in tasks:
            file_name = task.get('file', 'main.py')
            description = task.get('description', 'Implementacja')

            prompt = f"""
            Stwórz zawartość pliku: {file_name}
            Opis: {description}
            Technologie: {dream_result.get('technologies', [])}

            Podaj tylko kod, bez komentarzy markdown:
            """

            code = self.ask_ollama(prompt)
            # Usuń markdown formatting
            code = code.replace('```python', '').replace('```', '').strip()
            files[file_name] = code

        return {"files": files}

    def inception(self, problem: str) -> Dict:
        """Główna funkcja - wykonuje wszystkie 3 poziomy"""
        print(f"🌀 Inception starting for: {problem}")

        # Level 1: LIMBO
        print("📊 Level 1: LIMBO - Meta Architecture...")
        limbo_result = self.limbo(problem)
        print(f"   Components: {limbo_result.get('components', [])}")

        # Level 2: DREAM
        print("🎭 Level 2: DREAM - Solution Design...")
        dream_result = self.dream(limbo_result)
        print(f"   Architecture: {dream_result.get('architecture', 'N/A')}")

        # Level 3: REALITY
        print("🌍 Level 3: REALITY - Implementation...")
        reality_result = self.reality(dream_result)
        print(f"   Files: {list(reality_result.get('files', {}).keys())}")

        return {
            "problem": problem,
            "limbo": limbo_result,
            "dream": dream_result,
            "reality": reality_result
        }


def simple_cli():
    """Prosty CLI interface"""
    print("🌀 Simple Dream Architect")
    print("=" * 30)

    # Sprawdź połączenie z Ollama
    architect = SimpleDreamArchitect()
    try:
        test = architect.ask_ollama("test")
        print("✅ Ollama connection: OK")
    except:
        print("❌ Ollama connection: FAILED")
        print("   Make sure Ollama is running: ollama serve")
        return

    while True:
        problem = input("\n🎯 Describe your problem (or 'quit'): ").strip()

        if problem.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break

        if not problem:
            continue

        # Wykonaj inception
        result = architect.inception(problem)

        # Pokaż rezultaty
        print("\n" + "=" * 50)
        print("📋 RESULTS:")
        print("=" * 50)

        print("\n🏗️ ARCHITECTURE:")
        print(f"   {result['dream'].get('architecture', 'N/A')}")

        print("\n💻 TECHNOLOGIES:")
        for tech in result['dream'].get('technologies', []):
            print(f"   • {tech}")

        print("\n📁 GENERATED FILES:")
        for filename, content in result['reality'].get('files', {}).items():
            print(f"\n--- {filename} ---")
            print(content[:200] + "..." if len(content) > 200 else content)

        # Opcje
        save = input("\n💾 Save files? (y/n): ").lower()
        if save == 'y':
            import os
            os.makedirs("output", exist_ok=True)

            for filename, content in result['reality'].get('files', {}).items():
                with open(f"output/{filename}", 'w') as f:
                    f.write(content)
                print(f"   ✅ Saved: output/{filename}")


# Quick functions
def quick_solution(problem: str) -> Dict:
    """Jedna funkcja do szybkiego użycia"""
    architect = SimpleDreamArchitect()
    return architect.inception(problem)


def just_code(problem: str) -> Dict:
    """Tylko kod, bez verbose output"""
    architect = SimpleDreamArchitect()

    limbo = architect.limbo(problem)
    dream = architect.dream(limbo)
    reality = architect.reality(dream)

    return reality.get('files', {})


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Command line usage
        problem = " ".join(sys.argv[1:])
        result = quick_solution(problem)

        print("Generated files:")
        for filename, content in result['reality'].get('files', {}).items():
            print(f"\n=== {filename} ===")
            print(content)
    else:
        # Interactive CLI
        simple_cli()
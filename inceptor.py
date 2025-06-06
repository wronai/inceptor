#!/usr/bin/env python3
"""
Najprostszy Dream Architect System
Minimal implementation z Ollama integration
"""

import json
import requests
from typing import Dict, List
from datetime import datetime


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


    def simple_cli(self, problem: str):
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

            # Auto-save z opcjami
            save_choice = input("\n💾 Save files? (y/auto/custom/n): ").lower()

            if save_choice in ['y', 'yes', 'auto']:
                saved_files = self.save_files(result, auto_name=True)
                for filepath in saved_files:
                    print(f"   ✅ Saved: {filepath}")

            elif save_choice in ['custom', 'c']:
                project_name = input("📁 Project name: ").strip() or "project"
                saved_files = self.save_files(result, project_name=project_name)
                for filepath in saved_files:
                    print(f"   ✅ Saved: {filepath}")

    def save_files(self, result: Dict, project_name: str = None, auto_name: bool = False) -> List[str]:
        """Zapisuje wygenerowane pliki do dysku"""
        import os
        from datetime import datetime

        # Określ nazwę projektu
        if auto_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            project_name = f"dream_project_{timestamp}"
        elif not project_name:
            project_name = "output"

        # Stwórz katalog projektu
        project_dir = os.path.join("projects", project_name)
        os.makedirs(project_dir, exist_ok=True)

        saved_files = []
        files = result.get('reality', {}).get('files', {})

        # Zapisz pliki kodu
        for filename, content in files.items():
            filepath = os.path.join(project_dir, filename)

            # Stwórz subdirectories jeśli potrzebne
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            saved_files.append(filepath)

        # Zapisz metadata projektu
        metadata = {
            "problem": result.get('problem', ''),
            "timestamp": datetime.now().isoformat(),
            "architecture": result.get('dream', {}).get('architecture', ''),
            "technologies": result.get('dream', {}).get('technologies', []),
            "components": result.get('limbo', {}).get('components', []),
            "files": list(files.keys())
        }

        metadata_file = os.path.join(project_dir, "project_info.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        saved_files.append(metadata_file)

        # Stwórz README
        readme_content = self.generate_readme(result)
        readme_file = os.path.join(project_dir, "README.md")
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        saved_files.append(readme_file)

        return saved_files

    def generate_readme(self, result: Dict) -> str:
        """Generuje README.md dla projektu"""
        problem = result.get('problem', 'Unknown Problem')
        architecture = result.get('dream', {}).get('architecture', 'No architecture description')
        technologies = result.get('dream', {}).get('technologies', [])
        components = result.get('limbo', {}).get('components', [])
        files = list(result.get('reality', {}).get('files', {}).keys())

        readme = f"""# {problem.title()}

## Problem Description
{problem}

## Architecture
{architecture}

## Technologies Used
{chr(10).join(f"- {tech}" for tech in technologies)}

## Components
{chr(10).join(f"- {comp}" for comp in components)}

## Generated Files
{chr(10).join(f"- `{file}`" for file in files)}

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt  # if exists
```

2. Run the application:
```bash
python main.py  # or appropriate entry point
```

## Generated by Dream Architect
This project was automatically generated using the Dream Architect system.

- **Generation Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Levels Used**: LIMBO → DREAM → REALITY
"""
        return readme



# Enhanced save functions
def save_solution(problem: str, auto_save: bool = True) -> List[str]:
    """Generuje i automatycznie zapisuje rozwiązanie"""
    architect = SimpleDreamArchitect()
    result = architect.inception(problem)

    if auto_save:
        return architect.save_files(result, auto_name=True)
    return []


def batch_generate(problems: List[str], output_dir: str = "batch_projects") -> Dict[str, List[str]]:
    """Generuje rozwiązania dla wielu problemów na raz"""
    import os

    os.makedirs(output_dir, exist_ok=True)
    architect = SimpleDreamArchitect()
    results = {}

    for i, problem in enumerate(problems, 1):
        print(f"\n🌀 Processing {i}/{len(problems)}: {problem[:50]}...")

        try:
            result = architect.inception(problem)
            project_name = f"project_{i:02d}_{problem[:20].replace(' ', '_')}"
            project_name = "".join(c for c in project_name if c.isalnum() or c in '_-')

            saved_files = architect.save_files(result, project_name=project_name)
            results[problem] = saved_files
            print(f"   ✅ Saved to: projects/{project_name}")

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results[problem] = []

    return results


def list_projects() -> List[str]:
    """Lista wygenerowanych projektów"""
    import os

    if not os.path.exists("projects"):
        return []

    projects = []
    for item in os.listdir("projects"):
        project_path = os.path.join("projects", item)
        if os.path.isdir(project_path):
            projects.append(item)

    return sorted(projects)


def show_project_info(project_name: str):
    """Pokazuje informacje o projekcie"""
    import os

    info_file = os.path.join("projects", project_name, "project_info.json")

    if not os.path.exists(info_file):
        print(f"❌ Project {project_name} not found")
        return

    with open(info_file, 'r', encoding='utf-8') as f:
        info = json.load(f)

    print(f"\n📁 Project: {project_name}")
    print(f"🎯 Problem: {info.get('problem', 'N/A')}")
    print(f"🕒 Created: {info.get('timestamp', 'N/A')}")
    print(f"🏗️ Architecture: {info.get('architecture', 'N/A')}")
    print(f"💻 Technologies: {', '.join(info.get('technologies', []))}")
    print(f"📄 Files: {', '.join(info.get('files', []))}")


# Enhanced CLI with project management
def enhanced_cli():
    """Enhanced CLI z project management"""
    print("🌀 Dream Architect Pro")
    print("=" * 30)

    # Sprawdź połączenie z Ollama
    architect = SimpleDreamArchitect()
    try:
        test = architect.ask_ollama("test")
        print("✅ Ollama connection: OK")
    except:
        print("❌ Ollama connection: FAILED")
        return

    # Pokaż istniejące projekty
    projects = list_projects()
    if projects:
        print(f"\n📁 Existing projects ({len(projects)}):")
        for project in projects[-5:]:  # Show last 5
            print(f"   • {project}")
        if len(projects) > 5:
            print(f"   ... and {len(projects) - 5} more")

    while True:
        print("\n" + "=" * 50)
        print("Commands:")
        print("  dream <problem>  - Generate new solution")
        print("  batch           - Generate multiple solutions")
        print("  list            - List all projects")
        print("  show <project>  - Show project info")
        print("  quit            - Exit")

        command = input("\n🎯 Enter command: ").strip()

        if command.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break

        parts = command.split(None, 1)
        cmd = parts[0].lower() if parts else ""

        if cmd == "dream" and len(parts) > 1:
            problem = parts[1]
            result = architect.inception(problem)

            # Show results
            print("\n" + "=" * 50)
            print("📋 RESULTS:")
            print("=" * 50)

            print(f"\n🏗️ ARCHITECTURE:")
            print(f"   {result['dream'].get('architecture', 'N/A')}")

            print(f"\n💻 TECHNOLOGIES:")
            for tech in result['dream'].get('technologies', []):
                print(f"   • {tech}")

            print(f"\n📁 GENERATED FILES:")
            for filename in result['reality'].get('files', {}):
                print(f"   • {filename}")

            # Auto-save
            saved_files = architect.save_files(result, auto_name=True)
            print(f"\n💾 Auto-saved to:")
            for filepath in saved_files:
                print(f"   ✅ {filepath}")

        elif cmd == "batch":
            problems = []
            print("\nEnter problems (empty line to finish):")
            while True:
                problem = input("  > ").strip()
                if not problem:
                    break
                problems.append(problem)

            if problems:
                results = batch_generate(problems)
                print(f"\n✅ Generated {len([r for r in results.values() if r])} projects")

        elif cmd == "list":
            projects = list_projects()
            if projects:
                print(f"\n📁 Projects ({len(projects)}):")
                for project in projects:
                    print(f"   • {project}")
            else:
                print("\n📁 No projects found")

        elif cmd == "show" and len(parts) > 1:
            show_project_info(parts[1])

        else:
            print("❌ Unknown command or missing arguments")


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Command line usage
        problem = " ".join(sys.argv[1:])

        # Check for save flag
        if "--save" in sys.argv:
            print(f"🌀 Generating and saving solution for: {problem}")
            saved_files = save_solution(problem, auto_save=True)
            print("Generated files:")
            for filepath in saved_files:
                print(f"   ✅ {filepath}")

    else:
        # Interactive CLI
        enhanced_cli()
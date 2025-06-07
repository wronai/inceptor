import json
from typing import Dict, Any, Optional

from .ollama_client import OllamaClient
from .context_extractor import ContextExtractor
from .prompt_templates import PromptTemplates
from .models import Solution, Task
from .enums import ArchitectureLevel

class DreamArchitect:
    """Main class for generating multi-level solution architectures."""

    def __init__(self, ollama_url: str = "http://localhost:11434"):
        """Initialize the DreamArchitect with required components.
        
        Args:
            ollama_url: Base URL for the Ollama API server
        """
        self.ollama = OllamaClient(ollama_url)
        self.context_extractor = ContextExtractor()

    def inception(self, problem: str, max_levels: int = 3, additional_context: Optional[Dict[str, Any]] = None) -> Solution:
        """Generate a multi-level architecture solution.
        
        Args:
            problem: Problem description (one or more sentences)
            max_levels: Maximum depth of architecture (3-5)
            additional_context: Additional context information
            
        Returns:
            Solution object with complete architecture
        """
        if max_levels < 3 or max_levels > 5:
            raise ValueError("max_levels must be between 3 and 5")
            
        # Extract and enrich context
        context = self.context_extractor.extract_context(problem)
        if additional_context:
            context = self.context_extractor.enrich_context(context, additional_context)
        
        # Initialize solution
        solution = Solution(
            problem=problem,
            architecture={},
            tasks=[],
            implementation={},
            metadata={"context": context, "max_levels": max_levels}
        )
        
        # Execute each level of the architecture
        limbo_result = self._execute_limbo(problem, context)
        solution.architecture["limbo"] = limbo_result
        solution.tasks.extend(limbo_result.get("dream_tasks", []))
        
        if max_levels >= 2:
            dream_results = self._execute_dream(limbo_result, context)
            solution.architecture["dream"] = dream_results
            solution.tasks.extend(dream_results.get("reality_tasks", []))
            
            if max_levels >= 3:
                reality_results = self._execute_reality(dream_results, context)
                solution.implementation["reality"] = reality_results
                solution.tasks.extend(reality_results.get("deeper_tasks", []))
                
                if max_levels >= 4:
                    deeper_results = self._execute_deeper(reality_results, context)
                    solution.implementation["deeper"] = deeper_results
                    solution.tasks.extend(deeper_results.get("deepest_tasks", []))
                    
                    if max_levels >= 5:
                        deepest_results = self._execute_deepest(solution, context)
                        solution.implementation["deepest"] = deepest_results
        
        return solution

    def _execute_limbo(self, problem: str, context: Dict) -> Dict:
        """Execute Level 1 - Meta Architecture."""
        prompt = PromptTemplates.get_prompt(
            level=1,
            problem=problem,
            context=json.dumps(context, indent=2, ensure_ascii=False)
        )
        response = self.ollama.generate(prompt)
        return self._parse_json_response(response)

    def _execute_dream(self, limbo_result: Dict, context: Dict) -> Dict:
        """Execute Level 2 - Solution Design."""
        components = json.dumps(limbo_result.get("components", []), indent=2, ensure_ascii=False)
        dream_tasks = limbo_result.get("dream_tasks", [])
        
        results = {}
        for task in dream_tasks:
            prompt = PromptTemplates.get_prompt(
                level=2,
                task=json.dumps(task, indent=2, ensure_ascii=False),
                context=json.dumps(context, indent=2, ensure_ascii=False),
                components=components
            )
            response = self.ollama.generate(prompt)
            results[task["task_id"]] = self._parse_json_response(response)
        
        return results

    def _execute_reality(self, dream_results: Dict, context: Dict) -> Dict:
        """Execute Level 3 - Implementation."""
        results = {}
        for task_id, design in dream_results.items():
            for task in design.get("reality_tasks", []):
                prompt = PromptTemplates.get_prompt(
                    level=3,
                    task=json.dumps(task, indent=2, ensure_ascii=False),
                    specification=json.dumps(design["design"], indent=2, ensure_ascii=False),
                    context=json.dumps(context, indent=2, ensure_ascii=False)
                )
                response = self.ollama.generate(prompt)
                results[task["task_id"]] = self._parse_json_response(response)
        return results

    def _execute_deeper(self, reality_results: Dict, context: Dict) -> Dict:
        """Execute Level 4 - Integration."""
        results = {}
        for task_id, impl in reality_results.items():
            prompt = PromptTemplates.get_prompt(
                level=4,
                task=json.dumps(impl, indent=2, ensure_ascii=False),
                context=json.dumps(context, indent=2, ensure_ascii=False)
            )
            response = self.ollama.generate(prompt)
            results[task_id] = self._parse_json_response(response)
        return results

    def _execute_deepest(self, solution: Solution, context: Dict) -> Dict:
        """Execute Level 5 - Optimization."""
        results = {}
        for task_id, deeper in solution.implementation.get("deeper", {}).items():
            prompt = PromptTemplates.get_prompt(
                level=5,
                task=json.dumps(deeper, indent=2, ensure_ascii=False),
                context=json.dumps(context, indent=2, ensure_ascii=False)
            )
            response = self.ollama.generate(prompt)
            results[task_id] = self._parse_json_response(response)
        return results

    @staticmethod
    def _parse_json_response(response: str) -> Dict:
        """Parse JSON response from Ollama, handling potential formatting issues."""
        try:
            # Try to find JSON content between ```json and ```
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            # Try to find JSON content between ``` and ```
            elif "```" in response:
                json_str = response.split("```")[1].strip()
                if json_str.startswith("json"):
                    json_str = json_str[4:].strip()
                return json.loads(json_str)
            # Try to parse the whole response as JSON
            else:
                return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}\nResponse: {response}")

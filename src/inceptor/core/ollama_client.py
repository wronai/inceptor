import requests
from typing import Optional

class OllamaClient:
    """Client for communicating with Ollama Mistral:7b API."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        """Initialize the Ollama client.
        
        Args:
            base_url: Base URL of the Ollama API server
        """
        self.base_url = base_url
        self.model = "mistral:7b"

    def generate(self, prompt: str, system_prompt: str = "", max_tokens: int = 2000) -> str:
        """Generate a response from Ollama.
        
        Args:
            prompt: The input prompt for generation
            system_prompt: System prompt to guide the model's behavior
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If there's an error with the API request
        """
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

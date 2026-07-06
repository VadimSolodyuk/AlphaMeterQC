"""
AI Service Module for AlphaMeterQC.
Provides integration with Ollama local AI server.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import requests
except ImportError:
    raise ImportError(
        "Library 'requests' is required. Install it with: pip install requests"
    )

logger = logging.getLogger(__name__)


class OllamaService:
    """
    Service for interacting with Ollama AI API.

    This service provides methods to send requests to a local Ollama instance
    and receive AI-generated responses. Configuration is loaded from .env file.

    Example:
        >>> service = OllamaService()
        >>> response = service.generate("Explain SOLID principles")
        >>> print(response)
    """

    def __init__(self, env_path: Optional[Path] = None):
        """
        Initialize Ollama service.

        Args:
            env_path: Path to .env file. If None, searches in project root.
        """
        # Load environment variables
        if env_path is None:
            # Search for .env in project root
            project_root = Path(__file__).parent.parent.parent
            env_path = project_root / ".env"

        self.config = self._load_config(env_path)

        # Service configuration
        self.base_url = self.config.get("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = self.config.get("AI_MODEL", "qwen2.5:7b")
        self.timeout = int(self.config.get("AI_TIMEOUT", "120"))
        self.max_tokens = int(self.config.get("AI_MAX_TOKENS", "2048"))
        self.temperature = float(self.config.get("AI_TEMPERATURE", "0.7"))

        logger.info(f"OllamaService initialized: {self.base_url}, model: {self.model}")

    def _load_config(self, env_path: Path) -> Dict[str, str]:
        """
        Load configuration from .env file.

        Args:
            env_path: Path to .env file

        Returns:
            Dictionary with configuration values
        """
        config = {}
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith("#"):
                        continue
                    # Split by first '='
                    if "=" in line:
                        key, value = line.split("=", 1)
                        config[key.strip()] = value.strip()
        return config

    def check_connection(self) -> bool:
        """
        Check if Ollama API is available.

        Returns:
            True if API is accessible, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/version", timeout=5)
            if response.status_code == 200:
                version = response.json().get("version", "unknown")
                logger.info(f"Ollama API available, version: {version}")
                return True
            else:
                logger.error(f"API error: HTTP {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to Ollama API")
            return False
        except requests.exceptions.Timeout:
            logger.error("Connection timeout")
            return False

    def list_models(self) -> List[str]:
        """
        Get list of available models.

        Returns:
            List of model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [m["name"] for m in models]
            else:
                logger.error(f"Failed to get models: HTTP {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error getting models: {e}")
            return []

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """
        Generate AI response for given prompt.

        Args:
            prompt: User's question or instruction
            model: Model name (overrides default from config)
            max_tokens: Maximum tokens in response (overrides config)
            temperature: Generation temperature (overrides config)

        Returns:
            Generated text response

        Raises:
            ConnectionError: If Ollama API is not accessible
            TimeoutError: If request times out
            Exception: For other errors
        """
        # Use provided values or defaults from config
        model_name = model or self.model
        tokens = max_tokens or self.max_tokens
        temp = temperature if temperature is not None else self.temperature

        payload: dict[str, Any] = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temp, "num_predict": tokens},
        }

        try:
            logger.debug(f"Sending request to {model_name}: {prompt[:100]}...")
            response = requests.post(
                f"{self.base_url}/api/generate", json=payload, timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                answer: str = result.get("response", "")
                logger.debug(f"Response received: {len(answer)} chars")
                return answer
            else:
                error_msg = f"API error: HTTP {response.status_code}"
                logger.error(error_msg)
                raise Exception(error_msg)

        except requests.exceptions.Timeout:
            error_msg = f"Request timeout after {self.timeout}s"
            logger.error(error_msg)
            raise TimeoutError(error_msg)
        except requests.exceptions.ConnectionError:
            error_msg = "Failed to connect to Ollama API"
            logger.error(error_msg)
            raise ConnectionError(error_msg)
        except Exception as e:
            logger.error(f"Generation error: {e}")
            raise

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """
        Send chat-style request with conversation history.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (overrides default)
            temperature: Generation temperature (overrides config)

        Returns:
            AI response

        Example:
            >>> messages = [
            ...     {"role": "user", "content": "Hello!"}
            ... ]
            >>> response = service.chat(messages)
        """
        model_name = model or self.model
        temp = temperature if temperature is not None else self.temperature

        payload: dict[str, Any] = {
            "model": model_name,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temp},
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/chat", json=payload, timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                message = result.get("message", {})
                content = message.get("content", "")
                return str(content) if content else ""
            else:
                raise Exception(f"Chat API error: HTTP {response.status_code}")

        except requests.exceptions.Timeout:
            raise TimeoutError(f"Chat request timeout after {self.timeout}s")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Failed to connect to Ollama API")


# Convenience function for quick usage
def create_service(env_path: Optional[Path] = None) -> OllamaService:
    """
    Create and return configured OllamaService instance.

    Args:
        env_path: Optional path to .env file

    Returns:
        Configured OllamaService instance
    """
    return OllamaService(env_path)

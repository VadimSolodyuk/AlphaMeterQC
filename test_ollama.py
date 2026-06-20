#!/usr/bin/env python3
"""
Script for testing connection to Ollama API.
Checks the functionality of the local AI server.
"""

import sys
from pathlib import Path
from typing import Dict

# Add src to import path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    import requests
except ImportError:
    print("❌ Library 'requests' is not installed.")
    print("Install it with: pip install requests")
    sys.exit(1)


def load_env_file(env_path: Path) -> Dict[str, str]:
    """Load environment variables from .env file."""
    env_vars = {}
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
                    env_vars[key.strip()] = value.strip()
    return env_vars


def test_ollama_connection() -> bool:
    """Test connection to Ollama API."""
    # Load configuration from .env
    project_root = Path(__file__).parent
    env_path = project_root / ".env"

    print("=" * 60)
    print("OLLAMA CONNECTION TESTING")
    print("=" * 60)

    # Load environment variables
    env_vars = load_env_file(env_path)

    ollama_url = env_vars.get("OLLAMA_BASE_URL", "http://localhost:11434")
    model_name = env_vars.get("AI_MODEL", "qwen2.5:7b")

    print(f"\n📍 Ollama API URL: {ollama_url}")
    print(f"🤖 Model: {model_name}")
    print()

    # Check API availability
    try:
        response = requests.get(f"{ollama_url}/api/version", timeout=5)
        if response.status_code == 200:
            version_info = response.json()
            print("✅ Ollama API is available!")
            print(f"   Version: {version_info.get('version', 'unknown')}")
        else:
            print(f"❌ Error requesting version: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Failed to connect to Ollama API.")
        print("   Make sure Ollama is running:")
        print("   - Command: ollama serve")
        print("   - Or check systemd: systemctl status ollama")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout connecting to Ollama API.")
        return False

    # Check for model availability
    try:
        response = requests.get(f"{ollama_url}/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]

            print(f"\n📦 Available models ({len(model_names)}):")
            for name in model_names:
                status = "✓" if name == model_name else " "
                print(f"   {status} {name}")

            if model_name not in model_names:
                print(f"\n⚠️  Model '{model_name}' not found!")
                print(f"   Install it with: ollama pull {model_name}")
                return False
            else:
                print(f"\n✅ Model '{model_name}' is available!")
        else:
            print(f"❌ Error getting model list: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        return False

    # Test request to model
    print("\n🧪 Sending test request...")
    try:
        payload = {
            "model": model_name,
            "prompt": "Hello! Write a short greeting.",
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 50},
        }

        response = requests.post(f"{ollama_url}/api/generate", json=payload, timeout=60)

        if response.status_code == 200:
            result = response.json()
            answer = result.get("response", "")
            print("\n✅ Model response:")
            print(f"   {answer}")
            print("\n" + "=" * 60)
            print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
            print("=" * 60)
            return True
        else:
            print(f"❌ Error generating response: HTTP {response.status_code}")
            print(f"   {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("❌ Timeout generating response from model.")
        print("   The model may be too large for your CPU.")
        return False
    except Exception as e:
        print(f"❌ Error during test request: {e}")
        return False


if __name__ == "__main__":
    success = test_ollama_connection()
    sys.exit(0 if success else 1)

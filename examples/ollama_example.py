#!/usr/bin/env python3
"""
Example script demonstrating OllamaService usage.
Shows how to integrate AI capabilities into AlphaMeterQC.
"""

import sys
from pathlib import Path

# Add src to import path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))  # noqa: E402

from alphameterqc.ai_service import OllamaService  # noqa: E402


def example_basic_usage() -> None:
    """Basic example: simple question and answer."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 60)

    # Create service instance
    service = OllamaService()

    # Check connection
    if not service.check_connection():
        print("❌ Cannot connect to Ollama. Make sure it's running:")
        print("   sudo systemctl start ollama")
        return

    # Simple question
    prompt = "What is SOLID principle in software development?"
    print(f"\n📝 Question: {prompt}\n")

    try:
        response = service.generate(prompt, max_tokens=200)
        print(f"💡 Answer:\n{response}")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_chat_mode() -> None:
    """Example with conversation history."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Chat Mode with History")
    print("=" * 60)

    service = OllamaService()

    if not service.check_connection():
        print("❌ Cannot connect to Ollama")
        return

    # Conversation with context
    messages = [
        {"role": "user", "content": "I'm learning Python."},
        {
            "role": "assistant",
            "content": "Great choice! Python is excellent for beginners.",
        },
        {"role": "user", "content": "What should I learn first?"},
    ]

    print("\n💬 Conversation:")
    for msg in messages:
        role = msg["role"].capitalize()
        print(f"   {role}: {msg['content']}")

    try:
        response = service.chat(messages)
        print(f"\n🤖 AI Response:\n{response}")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_different_models() -> None:
    """Example showing model selection."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Available Models")
    print("=" * 60)

    service = OllamaService()

    if not service.check_connection():
        print("❌ Cannot connect to Ollama")
        return

    # List available models
    models = service.list_models()

    if models:
        print(f"\n📦 Found {len(models)} model(s):")
        for i, model in enumerate(models, 1):
            print(f"   {i}. {model}")

        # Use specific model if available
        if "llama3.2:3b" in models:
            print("\n🧪 Testing with llama3.2:3b...")
            try:
                _ = service.generate(
                    "Say hello in Russian",
                    model="llama3.2:3b",
                    max_tokens=50,
                )
            except Exception as e:
                print(f"   ❌ Error: {e}")
    else:
        print("\n⚠️  No models found. Install one with: ollama pull qwen2.5:7b")


def example_error_handling() -> None:
    """Example showing proper error handling."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Error Handling")
    print("=" * 60)

    service = OllamaService()

    # Test with invalid model
    print("\n🧪 Testing error handling with non-existent model...")
    try:
        _ = service.generate(
            "Hello",
            model="nonexistent-model-xyz",
            max_tokens=50,
        )
    except ConnectionError as e:
        print(f"   ✓ ConnectionError caught: {e}")
    except TimeoutError as e:
        print(f"   ✓ TimeoutError caught: {e}")
    except Exception as e:
        print(f"   ✓ Exception caught: {type(e).__name__}: {e}")


def main() -> None:
    """Run all examples."""
    print("\n" + "🤖" * 30)
    print("OllamaService Examples for AlphaMeterQC")
    print("🤖" * 30 + "\n")

    # Run examples
    example_basic_usage()
    example_chat_mode()
    example_different_models()
    example_error_handling()

    print("\n" + "=" * 60)
    print("✅ All examples completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check docs/ollama_setup.md for detailed documentation")
    print("2. Run 'python3 test_ollama.py' to verify setup")
    print("3. Integrate OllamaService into your application")


if __name__ == "__main__":
    main()

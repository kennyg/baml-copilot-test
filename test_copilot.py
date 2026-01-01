#!/usr/bin/env python3
"""
Test script for BAML + GitHub Copilot via LiteLLM

Reads test_config.json to determine which models are available.
Run generate_clients.py first to discover available models.
"""

import json
import os
import sys
from pathlib import Path

# Set the API key for LiteLLM
os.environ["LITELLM_API_KEY"] = "sk-baml-copilot-test"

from baml_client.sync_client import b
from baml_client.types import CodeReview


def load_config() -> dict:
    """Load test configuration."""
    config_path = Path("test_config.json")
    if not config_path.exists():
        print("❌ test_config.json not found!")
        print("   Run: mise run discover")
        sys.exit(1)
    return json.loads(config_path.read_text())


def test_explain_concept(model_name: str):
    """Test basic completion."""
    print(f"\n{'=' * 60}")
    print(f"TEST: ExplainConcept ({model_name})")
    print("=" * 60)

    try:
        result = b.ExplainConcept("OAuth device flow authentication")
        print(f"\nResult:\n{result[:200]}...")
        print(f"\n✅ {model_name}: SUCCESS")
        return True
    except Exception as e:
        print(f"\n❌ {model_name}: FAILED - {e}")
        return False


def test_code_review():
    """Test structured output extraction."""
    print(f"\n{'=' * 60}")
    print("TEST: ReviewCode (Structured Output)")
    print("=" * 60)

    sample_code = '''
def calculate_total(items):
    total = 0
    for i in range(len(items)):
        total = total + items[i]["price"] * items[i]["quantity"]
    return total
'''

    try:
        result: CodeReview = b.ReviewCode(sample_code, "python")
        print(f"\nSummary: {result.summary}")
        print(f"Issues: {result.issues[:2]}...")
        print(f"Quality: {result.overall_quality}")
        print("\n✅ Structured Output: SUCCESS")
        return True
    except Exception as e:
        print(f"\n❌ Structured Output: FAILED - {e}")
        return False


def test_streaming():
    """Test streaming."""
    print(f"\n{'=' * 60}")
    print("TEST: Streaming")
    print("=" * 60)

    try:
        print("\nStreaming response: ", end="", flush=True)
        stream = b.stream.ExplainConcept("async iterators in Python")
        for chunk in stream:
            if chunk:
                print(".", end="", flush=True)
        result = stream.get_final_response()
        print(f"\n\nFinal result:\n{result[:150]}...")
        print("\n✅ Streaming: SUCCESS")
        return True
    except Exception as e:
        print(f"\n❌ Streaming: FAILED - {e}")
        return False


def main():
    config = load_config()
    available = config.get("available_models", [])
    primary = config.get("primary_model", "unknown")

    print("=" * 60)
    print("BAML + GitHub Copilot via LiteLLM - Integration Test")
    print("=" * 60)
    print(f"\nAvailable models: {', '.join(available)}")
    print(f"Primary model: {primary}")
    print("\nMake sure LiteLLM proxy is running on port 4000!")

    results = {}

    # Test basic completion
    results["Basic Completion"] = test_explain_concept(primary)

    # Test structured output
    results["Structured Output"] = test_code_review()

    # Test streaming
    results["Streaming"] = test_streaming()

    # Summary
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")

    all_passed = all(results.values())
    print("\n" + ("🎉 All tests passed!" if all_passed else "⚠️  Some tests failed"))

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

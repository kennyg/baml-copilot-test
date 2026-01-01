#!/usr/bin/env python3
"""List available models from GitHub Copilot via LiteLLM proxy."""

import httpx

# LiteLLM proxy settings
PROXY_URL = "http://localhost:4000"
API_KEY = "sk-baml-copilot-test"


def list_proxy_models():
    """Query available models from the LiteLLM proxy."""
    try:
        response = httpx.get(
            f"{PROXY_URL}/v1/models",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        print("Configured models in LiteLLM proxy:\n")
        for model in data.get("data", []):
            model_id = model.get("id", "unknown")
            print(f"  - {model_id}")

        return data
    except httpx.ConnectError:
        print("Error: Cannot connect to LiteLLM proxy at localhost:4000")
        print("Make sure the proxy is running: mise run proxy")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def test_model(model_name: str):
    """Test if a specific model works."""
    print(f"\n  Testing: {model_name}")
    try:
        response = httpx.post(
            f"{PROXY_URL}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": model_name,
                "messages": [{"role": "user", "content": "Say 'hi'"}],
                "max_tokens": 5,
            },
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            actual_model = data.get("model", "unknown")
            content = data["choices"][0]["message"]["content"]
            print(f"    ✅ Works! Model: {actual_model}")
            return True, actual_model
        else:
            error = response.json().get("error", {}).get("message", response.text)
            # Extract useful part of error
            if "not supported" in str(error):
                print(f"    ❌ Model not available on your subscription")
            else:
                print(f"    ❌ {str(error)[:80]}")
            return False, None
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return False, None


if __name__ == "__main__":
    print("=" * 60)
    print("GitHub Copilot Models Discovery")
    print("=" * 60 + "\n")

    list_proxy_models()

    print("\n" + "=" * 60)
    print("Testing configured models:")
    print("=" * 60)

    configured = ["copilot-gpt-4o", "copilot-claude-sonnet", "copilot-o1"]
    for model in configured:
        test_model(model)

    print("\n" + "=" * 60)
    print("Testing additional Claude model names:")
    print("=" * 60)

    # These go directly to github_copilot provider
    claude_variants = [
        "github_copilot/claude-3.7-sonnet",
        "github_copilot/claude-3.5-sonnet",
        "github_copilot/claude-sonnet-4",
        "github_copilot/claude-sonnet-4.5",
        "github_copilot/claude-3-7-sonnet",
        "github_copilot/claude-3-5-sonnet",
    ]

    for model in claude_variants:
        test_model(model)

    print("\n" + "=" * 60)
    print("Notes:")
    print("=" * 60)
    print("""
  - If Claude models show "not available on your subscription":
    1. Check your GitHub Copilot tier (Pro/Pro+/Business/Enterprise)
    2. Verify Claude is enabled in Copilot settings at:
       https://github.com/settings/copilot
    3. Claude may need to be enabled by your org admin
""")

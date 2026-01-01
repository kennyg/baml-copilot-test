#!/usr/bin/env python3
"""
Quick test to verify LiteLLM is responding before running BAML tests.
Run this BEFORE test_copilot.py to debug connection issues.
"""

import requests
import json

LITELLM_URL = "http://localhost:4000"
API_KEY = "sk-baml-copilot-test"

def check_health():
    """Check if LiteLLM is running"""
    try:
        resp = requests.get(
            f"{LITELLM_URL}/health",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=5,
        )
        print(f"✅ LiteLLM health check: {resp.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ LiteLLM not running! Start with:")
        print("   litellm --config litellm_config.yaml --port 4000")
        return False

def check_models():
    """List available models"""
    try:
        resp = requests.get(
            f"{LITELLM_URL}/v1/models",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=5
        )
        if resp.status_code == 200:
            models = resp.json().get("data", [])
            print(f"✅ Available models: {[m['id'] for m in models]}")
            return True
        else:
            print(f"⚠️  Models endpoint returned {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to list models: {e}")
        return False

def test_completion():
    """Test a simple completion"""
    try:
        resp = requests.post(
            f"{LITELLM_URL}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "copilot-gpt-4o",
                "messages": [{"role": "user", "content": "Say hello in JSON format"}],
                "max_tokens": 50
            },
            timeout=30
        )
        
        if resp.status_code == 200:
            result = resp.json()
            content = result["choices"][0]["message"]["content"]
            print(f"✅ Completion test passed!")
            print(f"   Response: {content[:100]}...")
            return True
        else:
            print(f"❌ Completion failed: {resp.status_code}")
            print(f"   {resp.text}")
            return False
    except Exception as e:
        print(f"❌ Completion error: {e}")
        return False

def main():
    print("="*50)
    print("LiteLLM + GitHub Copilot Connection Test")
    print("="*50 + "\n")
    
    if not check_health():
        return 1
    
    print()
    check_models()
    
    print()
    if test_completion():
        print("\n🎉 LiteLLM is ready! Now run: python test_copilot.py")
        return 0
    else:
        print("\n⚠️  Check LiteLLM logs for authentication issues")
        return 1

if __name__ == "__main__":
    exit(main())

# BAML + GitHub Copilot via LiteLLM

This is a proof-of-concept for using GitHub Copilot models with BoundaryML's BAML framework via LiteLLM as a proxy.

## Why This Approach?

BAML doesn't have native GitHub Copilot support because Copilot uses OAuth device flow authentication (interactive login). LiteLLM handles this auth flow and exposes an OpenAI-compatible API that BAML can use via `openai-generic`.

## Prerequisites

- Python 3.10+
- GitHub Copilot subscription (Individual, Business, or Enterprise)
- BAML CLI (`pip install baml-py`)

## Setup

### 1. Create virtual environment

```bash
cd baml-copilot-test
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 2. Generate BAML client

```bash
baml-cli generate
```

### 3. Start LiteLLM proxy (Terminal 1)

```bash
litellm --config litellm_config.yaml --port 4000
```

On first run, you'll see:
```
Please visit https://github.com/login/device and enter code XXXX-XXXX to authenticate.
```

Complete the device flow in your browser. The token is saved at `~/.config/litellm/github_copilot/`.

### 4. Run tests (Terminal 2)

```bash
python test_copilot.py
```

## Available Clients

| BAML Client | Copilot Model | Notes |
|-------------|---------------|-------|
| `CopilotGPT4o` | gpt-4o | Fast, good for most tasks |
| `CopilotClaude` | claude-3.5-sonnet | Good for analysis/writing |
| `CopilotO1` | o1 | Reasoning model (premium) |
| `CopilotFallback` | GPT-4o → Claude | Auto-fallback on failure |

## Enterprise Copilot

If you're on GitHub Copilot Enterprise, the API endpoint differs. LiteLLM should handle this automatically, but if you see endpoint errors, check:

```bash
cat ~/.config/litellm/github_copilot/api-key.json | jq '.endpoints.api'
```

If it shows `api.enterprise.githubcopilot.com`, you may need to verify LiteLLM is using this endpoint.

## Troubleshooting

### "missing Editor-Version header"

Add headers to the LiteLLM call:
```python
extra_headers={
    "editor-version": "vscode/1.85.1",
    "Copilot-Integration-Id": "vscode-chat"
}
```

### Device flow timeout

Check network connectivity. Known issue: https://github.com/BerriAI/litellm/issues/17065

### Token refresh issues

Delete cached tokens and re-authenticate:
```bash
rm -rf ~/.config/litellm/github_copilot/
litellm --config litellm_config.yaml --port 4000
```

## Next Steps

If this works, we should:
1. Open a docs PR to BoundaryML adding GitHub Copilot instructions
2. Consider a native BAML provider if there's enough demand

# BAML + GitHub Copilot via LiteLLM

Use GitHub Copilot models with BoundaryML's BAML framework via LiteLLM proxy.

## Why This Approach?

BAML doesn't have native GitHub Copilot support because Copilot uses OAuth device flow authentication. LiteLLM handles this auth flow and exposes an OpenAI-compatible API that BAML can use via `openai-generic`.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) - Python package manager
- [mise](https://mise.jdx.dev/) - Task runner
- GitHub Copilot subscription

## Quick Start

```bash
# Install dependencies
mise run setup

# Start LiteLLM proxy (in a separate terminal)
mise run proxy
# First run will prompt for GitHub device flow authentication

# Discover available models and generate configs
mise run discover

# Generate BAML client
mise run generate

# Run tests
mise run test
```

## Available Tasks

| Task | Description |
|------|-------------|
| `mise run setup` | Install dependencies with uv |
| `mise run proxy` | Start LiteLLM proxy on port 4000 |
| `mise run discover` | Discover available models & generate configs |
| `mise run generate` | Generate BAML client code |
| `mise run test` | Run integration tests |
| `mise run models` | List and test available models |
| `mise run clean` | Remove generated files |

## Model Discovery

The `discover` command tests which GitHub Copilot models your subscription can access:

```
Known GitHub Copilot models:
  - gpt-4o
  - gpt-4
  - o1
  - claude-3.7-sonnet
  - gemini-2.0-flash
  ...

Testing which models your subscription can access...

  gpt-4o... ✅
  claude-3.7-sonnet... ❌
  ...
```

Models availability depends on your Copilot tier:
- **Copilot Individual**: GPT-4o
- **Copilot Pro/Pro+**: GPT-4o, Claude, O1, Gemini (varies)
- **Copilot Business/Enterprise**: Configured by admin

## Generated Files

The `discover` command generates:

| File | Purpose |
|------|---------|
| `litellm_config.yaml` | LiteLLM proxy configuration |
| `baml_src/clients.baml` | BAML client definitions |
| `test_config.json` | Test configuration |

## Project Structure

```
├── mise.toml              # Task definitions
├── pyproject.toml         # Python dependencies (uv)
├── litellm_config.yaml    # LiteLLM proxy config (generated)
├── baml_src/
│   ├── clients.baml       # BAML clients (generated)
│   ├── functions.baml     # BAML functions
│   └── generators.baml    # BAML generator config
├── generate_clients.py    # Model discovery & config generator
├── test_copilot.py        # Integration tests
└── list_models.py         # Model listing utility
```

## Troubleshooting

### Device flow authentication

On first `mise run proxy`, complete the GitHub device flow:
```
Please visit https://github.com/login/device and enter code XXXX-XXXX
```

### Token refresh issues

Delete cached tokens and re-authenticate:
```bash
rm -rf ~/.config/litellm/github_copilot/
mise run proxy
```

### Model not available

Run `mise run discover` to see which models your subscription supports. Check your Copilot settings at https://github.com/settings/copilot.

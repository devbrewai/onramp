# 6. Lazy agent initialization

Date: 2026-04-09

## Status

Accepted

## Context

Pydantic AI's `Agent()` constructor immediately resolves the model provider, which requires an API key. If the agent is created at module import time (top-level), the module can't be imported without a valid API key — breaking `mypy`, `ruff`, `pytest` (for non-integration tests), and any other tool that imports the module graph.

## Decision

Use lazy initialization: the agent is stored as a module-level `None` and created on first use via `_get_agent()`. The API key is bridged from pydantic-settings (`.env`) to `os.environ` at agent creation time, since Pydantic AI providers read keys from `os.environ` directly.

```python
_agent: Agent[None, LLMExtractionResult] | None = None

def _get_agent() -> Agent[None, LLMExtractionResult]:
    global _agent
    if _agent is None:
        if settings.anthropic_api_key:
            os.environ.setdefault("ANTHROPIC_API_KEY", settings.anthropic_api_key)
        _agent = Agent(settings.llm_model, ...)
    return _agent
```

## Consequences

- Module imports cleanly without an API key — all tooling (mypy, ruff, pytest unit tests) works
- First request pays a one-time agent initialization cost (negligible)
- The `os.environ.setdefault` bridge is necessary because pydantic-settings loads `.env` into its own model, not into `os.environ`, while Pydantic AI's providers check `os.environ` directly
- If additional providers are added, their API keys need the same bridge pattern

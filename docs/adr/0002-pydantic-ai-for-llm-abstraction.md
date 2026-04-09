# 2. Pydantic AI as the provider-agnostic LLM layer

Date: 2026-04-09

## Status

Accepted

## Context

The extraction pipeline needs to call a vision-capable LLM and get back typed, structured data matching our Pydantic models. We evaluated five options:

| Library | Structured output | Vision | Providers | Type safety |
|---|---|---|---|---|
| **Pydantic AI** | Native Pydantic instances | BinaryContent | ~10 | Strong |
| **LiteLLM** | JSON string → manual parse | OpenAI-format image_url | 100+ | Good |
| **LangChain** | Dict (not Pydantic instance) | Multimodal content blocks | Many | Weak |
| **aisuite** | None | Undocumented | ~10 | Thin |
| **OpenRouter** | None (DIY) | OpenAI-format | All (proxy) | DIY |

## Decision

Use **Pydantic AI** (`pydantic-ai[anthropic]`).

- `Agent(model_string, output_type=PydanticModel)` returns a typed Pydantic instance, not a dict or JSON string
- Provider swap is one line: change `LLM_MODEL` env var from `anthropic:claude-sonnet-4-6` to `openai:gpt-4o` or `google-gla:gemini-2.5-flash`
- Vision input via `BinaryContent(data=png_bytes, media_type="image/png")` — same API across all providers
- Built-in `FallbackModel` for reliability chains if needed later
- Maintained by the Pydantic team, strong mypy compatibility

## Consequences

- Fewer supported providers than LiteLLM (~10 vs 100+), but covers all major ones (Anthropic, OpenAI, Google, Groq, Ollama)
- No built-in cost tracking (LiteLLM has this) — acceptable for a demo
- Adding a new provider is `uv add pydantic-ai[openai]` + change the env var, zero code changes
- If Pydantic AI's API changes, we're coupled to it — mitigated by the library's stability (v1.x, Pydantic team)

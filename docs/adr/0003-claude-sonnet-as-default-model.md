# 3. Claude Sonnet 4.6 as the default extraction model

Date: 2026-04-09

## Status

Accepted

## Context

The extraction pipeline needs a vision-capable model that returns accurate structured data. Candidates:

- `anthropic:claude-sonnet-4-6` — latest Anthropic Sonnet, strong vision, ~$3/MTok input
- `anthropic:claude-opus-4-6` — highest accuracy, 5-10x more expensive
- `openai:gpt-4o` — competitive vision, ~$2.50/MTok
- `google-gla:gemini-2.5-flash` — cheapest (~$0.075/MTok), fastest

## Decision

Default to `anthropic:claude-sonnet-4-6` via the `LLM_MODEL` environment variable. The model is configurable — swapping providers requires only changing the env var and installing the provider extra (e.g., `uv add pydantic-ai[openai]`).

## Consequences

- Sonnet balances accuracy and cost for demo-quality samples
- Real user uploads with noisy/low-quality documents may need Opus for edge cases — easy to switch
- Anthropic API key is required by default; other providers need their own keys
- ~12s per document extraction in testing — well within the 30s budget

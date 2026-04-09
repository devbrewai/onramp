# 4. Single LLM call for classification and extraction

Date: 2026-04-09

## Status

Accepted

## Context

The PRD specifies three steps: classify document type, extract fields, validate. Two approaches:

1. **Two calls**: first call classifies (`government_id`), second call extracts fields using a type-specific prompt
2. **Single call**: one prompt classifies AND extracts in the same request

## Decision

Use a **single LLM call** that returns `document_type`, `document_subtype`, and `fields[]` together. The Pydantic AI agent uses `LLMExtractionResult` as its output type, which includes both classification and extraction fields.

The Linear milestones "Document Classification" and "Field Extraction" were merged into one implementation milestone.

## Consequences

- Half the API calls, half the latency, half the cost per document
- Simpler code — one agent, one prompt, one response model
- The prompt is longer (includes all 3 document type schemas) but still within model context limits
- If classification accuracy suffers, we can't re-route to a type-specific extraction prompt — mitigated by strong results in testing (0.99 confidence on all 3 sample types)
- Validation remains a separate post-processing step (next milestone), not part of the LLM call

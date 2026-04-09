# Architecture Decision Records

This directory contains the Architecture Decision Records (ADRs) for the Onramp project. ADRs capture the context, decision, and consequences of significant architectural choices.

## Index

| # | Decision | Status |
|---|---|---|
| [0](0000-use-adrs.md) | Record architecture decisions | Accepted |
| [1](0001-llm-first-not-ocr-first.md) | LLM-first, not OCR-first pipeline | Accepted |
| [2](0002-pydantic-ai-for-llm-abstraction.md) | Pydantic AI as the provider-agnostic LLM layer | Accepted |
| [3](0003-claude-sonnet-as-default-model.md) | Claude Sonnet 4.6 as the default extraction model | Accepted |
| [4](0004-single-call-classify-and-extract.md) | Single LLM call for classification and extraction | Accepted |
| [5](0005-pymupdf-for-pdf-rendering.md) | PyMuPDF for PDF-to-image rendering | Accepted |
| [6](0006-lazy-agent-initialization.md) | Lazy agent initialization | Accepted |
| [7](0007-mypy-override-for-pymupdf.md) | Per-module mypy override for PyMuPDF stubs | Accepted |
| [8](0008-committed-sample-documents.md) | Committed sample documents with generator scripts | Accepted |

## Adding a new ADR

1. Copy an existing ADR as a template
2. Number it sequentially (next: `0009`)
3. Include: Context (the problem), Decision (what we chose), Consequences (trade-offs)
4. Set status to `Accepted`, `Superseded`, or `Deprecated`
5. Update this index

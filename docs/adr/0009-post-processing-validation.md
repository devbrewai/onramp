# 9. Post-processing validation with immutable field copies

Date: 2026-04-09

## Status

Accepted

## Context

The LLM returns confidence scores and risk flags, but these are probabilistic estimates. The PRD requires deterministic validation rules (date format checks, ID number format checks, expiration verification) that adjust confidence scores and compute an overall risk score.

Two approaches for where to validate:
1. Add validation instructions to the LLM prompt — more natural, but non-deterministic, untestable, and doubles the prompt length if done as a second call
2. Post-processing validation in Python — deterministic, unit-testable, auditable, zero API cost

For how to handle field modifications:
1. Mutate `ExtractedField` instances in-place — simple but destroys original LLM output
2. Create new instances via `model_copy(update={...})` — preserves originals, pure function semantics

## Decision

Validation is a **pure post-processing step** in `app/services/validator.py`. It takes the LLM's `LLMExtractionResult`, runs deterministic checks, and returns a `ValidationResult` with adjusted fields, risk score, and warnings.

Fields are never mutated in-place. Adjusted fields are created via Pydantic v2's `model_copy(update={...})`, preserving the original LLM output for debugging.

Required field schemas are defined as a `REQUIRED_FIELDS` constant in the validator module, mirroring the schemas in the LLM extraction prompt.

Six validation rules are applied in order:
1. Null value with nonzero confidence → force confidence to 0.0
2. Date format validation (YYYY-MM-DD) → reduce confidence by 0.15
3. ID number format check (min 5 chars) → reduce confidence by 0.20
4. `requires_review` enforcement → set based on 0.80 threshold
5. Server-side expiration check → correct `is_expired` if LLM disagrees
6. Missing required fields → add warnings per missing field

## Consequences

- All validation rules are unit-testable without an API key (33 tests, <0.1s)
- Risk scores are deterministic and auditable — same input always produces same output
- Confidence adjustments are traceable (original LLM value vs adjusted value)
- Required field schemas are duplicated between the prompt and the validator constant — must be kept in sync manually when adding new document types
- `model_copy` creates new instances (trivial memory cost for <15 fields per document)

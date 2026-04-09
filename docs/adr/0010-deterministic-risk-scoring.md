# 10. Deterministic risk scoring over LLM-based risk assessment

Date: 2026-04-09

## Status

Accepted

## Context

Risk scoring can be done by:
1. Asking the LLM to output a risk score as part of its extraction response
2. Computing it deterministically from confidence values and flags in Python

The LLM approach would require either a second prompt or extending the extraction prompt. The deterministic approach uses the PRD's explicit rules (§5) as a waterfall priority chain.

## Decision

Risk scoring is a **pure Python function** (`compute_risk_score`) that applies PRD §5 rules to the validated field confidences, expiration status, and missing-field checks:

- Any field < 0.70 confidence, expired document, or missing required fields → **high**
- Any field 0.70–0.90 confidence → **medium**
- All fields >= 0.90 confidence → **low**

The `>= 0.90` boundary (vs strict `> 0.90` in the PRD text) is a deliberate interpretation: 0.90 is a strong confidence score, and the PRD's phrasing ("All fields >90%") reads as a demo spec, not a compliance document. This is documented in a code comment.

The LLM is not involved in risk scoring at all.

## Consequences

- Deterministic: same inputs always produce the same risk score
- Testable: 9 unit test cases cover all boundary conditions (0.699 → high, 0.70 → medium, 0.90 → low)
- Auditable: the rules are visible in code, not buried in a prompt
- Zero additional API cost — risk scoring is pure computation
- Inflexible: adding nuanced risk assessment (e.g., "this looks like a high-quality forgery") would require either LLM involvement or additional heuristics. Acceptable trade-off for a demo where controlled samples always produce clean extractions.

# 0. Record architecture decisions

Date: 2026-04-09

## Status

Accepted

## Context

We need to record the architectural decisions made on this project so that future contributors can understand the trade-offs behind the codebase without re-discovering them through trial and error. This is especially important as an open source project where contributors won't have access to the original conversations.

## Decision

We will use Architecture Decision Records (ADRs) in the MADR format, stored in `docs/adr/`, numbered sequentially.

Each ADR captures: context (the problem), decision (what we chose), consequences (trade-offs), and status (accepted, superseded, deprecated).

## Consequences

- Every non-obvious architectural choice gets a short document explaining why
- Contributors can reference ADRs in PR reviews instead of re-explaining trade-offs
- Superseded decisions link to their replacements, preserving institutional memory
- Small overhead per decision (~5 min to write)

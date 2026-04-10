# 12. Simulated pipeline stages over real streaming

Date: 2026-04-10

## Status

Accepted

## Context

The PRD specifies a 4-stage verification pipeline animation (Upload, Classify, Extract, Validate). The backend processes documents in a single synchronous API call with no intermediate progress events. Two options: simulate stages with fixed timers, or add real SSE/streaming to the backend.

## Decision

Animate stages on **fixed timers** while the real API call runs in parallel. Stages 1-3 advance at 800ms, 1000ms, and 1700ms. Stage 4 completes only after the API response arrives — the animation never outruns the data.

The `usePipelineAnimation` custom hook accepts a `Promise<ProcessResponse>` and coordinates the timer sequence with the promise resolution.

## Consequences

- Polished UX that matches the PRD exactly — users see each stage animate in sequence
- Stage timings are approximate, not real processing phases
- Zero backend changes required — the single `POST /api/process` call is unchanged
- If real SSE/streaming is added later, the hook can be adapted to listen for server events instead of using timers, without changing the component tree

# 11. Native fetch over axios for API client

Date: 2026-04-10

## Status

Accepted

## Context

The frontend needs an HTTP client for 2 API endpoints (`POST /api/process`, `GET /api/samples`). Options: axios (29KB, rich feature set) or native `fetch` with a thin wrapper.

## Decision

Use native `fetch` wrapped in a 30-line typed module (`src/lib/api.ts`). The wrapper provides typed return values, centralized error handling, and an `ApiError` class.

## Consequences

- Zero additional runtime dependencies
- Type-safe API calls with `ProcessResponse` and `SampleInfo` return types
- No request interceptors, cancellation, or retry logic — not needed for 2 endpoints
- If the app grows to need interceptors or request cancellation, revisit with axios or ky

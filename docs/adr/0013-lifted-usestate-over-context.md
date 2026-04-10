# 13. Lifted useState over context or zustand

Date: 2026-04-10

## Status

Accepted

## Context

The dashboard needs shared state for the processing flow (`idle → processing → results → error`) and the applicant list. Options: React Context, Zustand, or lifted `useState` in the Dashboard component.

## Decision

Use `useState` in the Dashboard component with a **discriminated union** type:

```ts
type DashboardView =
  | { status: "idle" }
  | { status: "processing"; file: File | null; sampleId: string | null }
  | { status: "results"; result: ProcessResponse; previewUrl: string | null }
  | { status: "error"; message: string }
```

Child components receive state and callbacks via props (one level of drilling).

## Consequences

- Simple, explicit data flow — easy to trace state changes in the component tree
- TypeScript exhaustive checks via the discriminated union prevent impossible states
- Prop drilling is minimal (Dashboard → 4 direct children)
- No additional dependencies (no Zustand, no Context boilerplate)
- If the app added routing or deeply nested consumers, a Context or store would be needed. For a single-page demo, this is the right level of abstraction.

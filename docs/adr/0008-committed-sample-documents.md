# 8. Committed sample documents with generator scripts

Date: 2026-04-09

## Status

Accepted

## Context

The demo needs 3 realistic sample documents (passport, utility bill, pay stub) using the Jordan Taylor persona. Options:

1. **Commit binaries only** — hand-craft or AI-generate, commit to repo
2. **Generate at runtime** — produce on each request from templates
3. **Commit binaries + generator script** — script produces files, both committed

## Decision

Use approach 3: a Python script (`backend/scripts/generate_samples.py`) using fpdf2 and Pillow produces the three sample files, and both the script and the output binaries are committed to `backend/data/samples/`.

## Consequences

- Samples are regeneratable if we change persona data or fix formatting — run the script and re-commit
- No runtime dependency on sample generation — files are pre-built and served directly
- Binary files in git add ~45KB (1 PNG + 2 small PDFs) — negligible
- fpdf2 is a dev dependency only — not needed in production
- All sample data is fictional (Jordan Taylor persona) with consistent names/addresses across documents for cross-document validation testing

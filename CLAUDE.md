# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Onramp is a mock fintech onboarding platform with AI-powered KYC document intake. Users upload an identity, address, or income document and get back classified, extracted, and validated structured data with per-field confidence scores and an overall risk score.

## Tech Stack

- **Frontend:** React 19 + TypeScript + Vite + Tailwind CSS + shadcn/ui, Bun as package manager/runtime
- **Backend:** Python 3.11+ + FastAPI
- **LLM:** Anthropic Claude (vision-capable Sonnet) — single call handles classification + extraction
- **PDF/Image Parsing:** PyMuPDF (`fitz`) for PDF → image, Pillow for image handling
- **Deployment:** Vercel or Cloudflare Pages (frontend), Render (backend)

## Architecture

```
React Frontend
├── Mock Onramp Dashboard (top nav, stats cards, applicant queue)
├── Document Upload Area (drag-drop + sample document cards)
├── Verification Pipeline View (4-stage animated: upload → classify → extract → validate)
└── Results View (document preview + editable fields with confidence badges)
        │ multipart/form-data
FastAPI Backend
├── POST /api/process    → document processing pipeline
│   ├── File ingest (uploaded file OR sample_id)
│   ├── PDF → image conversion (PyMuPDF, if needed)
│   ├── LLM Vision Extraction (single Claude call)
│   │   ├── Classifies document_type
│   │   ├── Extracts fields[] with per-field confidence + source_text
│   │   └── Returns structured JSON
│   ├── Validator
│   │   ├── Date format checks (adjust confidence -0.15 on failure)
│   │   ├── ID number format checks (adjust confidence -0.20 on failure)
│   │   ├── Expiration check → risk flag
│   │   └── Cross-field name consistency
│   └── Risk Scorer (low/medium/high from confidence + flags)
├── GET  /api/samples    → list of pre-loaded sample documents
└── GET  /api/health     → status check
```

The pipeline is deliberately **LLM-first, not OCR-first**: Claude vision reads the document and extracts structured fields in a single call. Do not introduce Tesseract, AWS Textract, or any separate OCR step — this is both an accuracy and a "showcases modern AI" decision.

## Environment Variables

Backend `.env`:

- `ANTHROPIC_API_KEY` — Claude API key (required)
- `CORS_ORIGINS` — Allowed origins, comma-separated
- `MAX_FILE_SIZE_MB` — Upload size cap (default: `10`)
- `LOG_LEVEL` — Logging level (default: `info`)

Frontend `.env`:

- `VITE_API_URL` — Backend URL

## Development Workflow

All changes must be **atomic** and **methodological**. One logical change per unit of work.

### Principles

- **DRY** — Don't Repeat Yourself; extract shared logic, avoid copy-paste
- **Single Responsibility** — each function, file, and module does one thing well
- **Clean Code** — meaningful names, small functions, no dead code, no magic numbers
- **YAGNI** — don't build what isn't needed yet
- **Separation of Concerns** — keep layers distinct (routes, services, data)

Every change follows this flow:

1. **Code** — make one atomic, focused change
2. **Lint** — backend: `ruff check . && ruff format --check .` / frontend: `bun run lint`
3. **Type-check** — backend: `mypy .` / frontend: `bunx tsc --noEmit`
4. **Test** — backend: `pytest` / frontend: `bun test`
5. **Commit** — one commit per logical change (see commit conventions below)

Do not skip steps. Do not batch unrelated changes into a single commit. If lint, type-check, or tests fail, fix before committing.

## Git Commit Conventions

Follow Angular conventional commit format:

- **Format:** `<type>(<scope>): <subject>`
- **Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- **Scope:** optional, e.g. `chat`, `rag`, `dashboard`, `widget`, `api`, `tools`
- **Subject:** imperative mood, lowercase, no period at end, max 50 chars
- **Body:** use bullet points to explain what and why
  - Each bullet starts with `-`
  - Wrap at 72 characters
- **Breaking changes:** add `BREAKING CHANGE:` in the footer
- **No AI attribution:** do not include `Co-Authored-By` or any AI/Claude attribution lines

### Examples

```
feat(rag): add document chunking with overlap

- Chunk knowledge base files into 300-500 token segments
- Use 50-token overlap to preserve context across boundaries
- Store chunks in ChromaDB collection on startup
```

```
fix(chat): handle empty SSE stream without crashing

- Check for empty response before parsing SSE events
- Add fallback error message when stream closes unexpectedly
```

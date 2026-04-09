# 5. PyMuPDF for PDF-to-image rendering

Date: 2026-04-09

## Status

Accepted

## Context

PDFs need to be converted to PNG images before sending to the vision LLM. Options:

- **PyMuPDF** (`pymupdf`/`fitz`) — pure Python bindings to MuPDF, renders pages to pixmaps, pip-installable
- **pdf2image** + Poppler — requires system-level Poppler installation, harder to deploy
- **Pillow** — can't render PDFs natively
- **Claude native PDF** — some models accept PDF bytes directly, but not consistently across all providers

## Decision

Use **PyMuPDF** (`pymupdf`). Render each page at 200 DPI via `page.get_pixmap(dpi=200).tobytes("png")`, capped at 3 pages per document.

## Consequences

- Pure `pip install` — no system dependencies, easy CI/CD and containerization
- 200 DPI is sufficient for LLM vision without excessive file sizes (~200-400KB per page)
- 3-page cap prevents abuse and keeps processing time bounded
- PyMuPDF's type stubs are incomplete (`py.typed` shipped but `open`, `close`, `tobytes` are untyped) — handled with a scoped mypy override on `app.services.converter` rather than inline `type: ignore` comments
- If we later need provider-native PDF support, we can add a bypass path without removing the PyMuPDF fallback

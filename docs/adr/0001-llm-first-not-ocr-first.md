# 1. LLM-first, not OCR-first pipeline

Date: 2026-04-07

## Status

Accepted

## Context

Document processing systems traditionally use a multi-stage pipeline: OCR (Tesseract, AWS Textract, Google Document AI) extracts raw text, then a classifier and parser operate on that text. This is well-understood but adds complexity (OCR config, layout analysis, text normalization) and fails on non-standard layouts.

Modern vision-capable LLMs (Claude, GPT-4o, Gemini) can read documents directly from images and extract structured data in a single call.

## Decision

The entire extraction pipeline is a **single LLM vision call**. Documents are converted to PNG images and sent directly to Claude, which classifies the document type AND extracts all fields in one pass.

We do not use Tesseract, AWS Textract, or any separate OCR step.

## Consequences

- Simpler architecture: no OCR dependencies, no text normalization, no layout analysis
- Higher accuracy on varied layouts — the LLM handles formatting implicitly
- Showcases modern AI approach (important for a Devbrew portfolio demo)
- Higher per-call cost vs. OCR-then-classify (~$0.01-0.03 per document with Sonnet)
- Dependent on LLM vision quality — if the model hallucinates a field, there's no OCR ground truth to compare against
- PDF→image conversion (PyMuPDF) is the only preprocessing step

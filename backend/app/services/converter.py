"""Normalize uploaded documents into PNG images for LLM vision input."""

from __future__ import annotations

import io

import pymupdf
from PIL import Image

MAX_PAGES = 3
PDF_DPI = 200
IMAGE_CONTENT_TYPES = {"image/png", "image/jpeg", "image/jpg"}


def to_images(file_bytes: bytes, content_type: str) -> list[bytes]:
    """Convert a file to a list of PNG byte arrays (one per page, max 3).

    Supported content types:
    - image/png, image/jpeg → re-encode to PNG for consistency
    - application/pdf → render each page via PyMuPDF at 200 DPI
    """
    if content_type in IMAGE_CONTENT_TYPES:
        return [_image_to_png(file_bytes)]

    if content_type == "application/pdf":
        return _pdf_to_pngs(file_bytes)

    msg = f"Unsupported content type: {content_type}"
    raise ValueError(msg)


def _image_to_png(data: bytes) -> bytes:
    """Re-encode any supported image format to PNG bytes."""
    buf = io.BytesIO()
    with Image.open(io.BytesIO(data)) as img:
        img.save(buf, format="PNG")
    return buf.getvalue()


def _pdf_to_pngs(data: bytes) -> list[bytes]:
    """Render PDF pages to PNG bytes via PyMuPDF, capped at MAX_PAGES."""
    doc = pymupdf.open(stream=data, filetype="pdf")
    pages: list[bytes] = []
    for i in range(min(len(doc), MAX_PAGES)):
        page = doc[i]
        pix = page.get_pixmap(dpi=PDF_DPI)
        pages.append(pix.tobytes("png"))
    doc.close()
    return pages

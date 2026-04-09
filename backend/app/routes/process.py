"""POST /api/process — document processing pipeline endpoint."""

from __future__ import annotations

import time
import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, UploadFile

from app.config import settings
from app.models.document import ProcessResponse
from app.services.converter import to_images
from app.services.extractor import extract_document

router = APIRouter()

SAMPLES_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "samples"

SAMPLE_FILES: dict[str, tuple[str, str]] = {
    "sample_passport": ("sample_passport.png", "image/png"),
    "sample_utility_bill": ("sample_utility_bill.pdf", "application/pdf"),
    "sample_pay_stub": ("sample_pay_stub.pdf", "application/pdf"),
}


@router.post("/process", response_model=ProcessResponse)
async def process_document(
    file: UploadFile | None = None,
    sample_id: Annotated[str | None, Form()] = None,
) -> ProcessResponse:
    """Process a document through the classification + extraction pipeline."""
    start = time.perf_counter()

    file_bytes, content_type = await _resolve_input(file, sample_id)

    images = to_images(file_bytes, content_type)
    # Process only the first page for extraction
    result = await extract_document(images[0])

    elapsed_ms = int((time.perf_counter() - start) * 1000)

    return ProcessResponse(
        id=str(uuid.uuid4()),
        document_type=result.document_type,
        document_subtype=result.document_subtype,
        document_type_confidence=result.document_type_confidence,
        is_expired=result.is_expired,
        processing_time_ms=elapsed_ms,
        fields=result.fields,
        risk_flags=result.risk_flags,
    )


async def _resolve_input(
    file: UploadFile | None,
    sample_id: str | None,
) -> tuple[bytes, str]:
    """Resolve the input to (file_bytes, content_type)."""
    if sample_id:
        return _load_sample(sample_id)

    if file:
        return await _read_upload(file)

    raise HTTPException(status_code=400, detail="Provide either 'file' or 'sample_id'.")


def _load_sample(sample_id: str) -> tuple[bytes, str]:
    """Load a pre-built sample document by ID."""
    if sample_id not in SAMPLE_FILES:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown sample_id: {sample_id}",
        )

    filename, content_type = SAMPLE_FILES[sample_id]
    path = SAMPLES_DIR / filename

    if not path.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Sample file not found on disk: {filename}",
        )

    return path.read_bytes(), content_type


async def _read_upload(file: UploadFile) -> tuple[bytes, str]:
    """Read and validate an uploaded file."""
    content_type = file.content_type or "application/octet-stream"
    data = await file.read()

    max_bytes = settings.max_file_size_mb * 1024 * 1024
    if len(data) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds {settings.max_file_size_mb}MB limit.",
        )

    return data, content_type

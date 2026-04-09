from typing import Literal

from pydantic import BaseModel, Field

DocumentType = Literal["government_id", "proof_of_address", "income_verification"]


class ExtractedField(BaseModel):
    """A single field extracted from a document."""

    field_name: str
    label: str
    value: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    source_text: str | None = None
    requires_review: bool = False


class LLMExtractionResult(BaseModel):
    """Raw structured output from the LLM vision call."""

    document_type: DocumentType
    document_subtype: str
    document_type_confidence: float = Field(ge=0.0, le=1.0)
    is_expired: bool
    fields: list[ExtractedField]
    risk_flags: list[str] = []


class ProcessResponse(BaseModel):
    """API response wrapping the LLM extraction with metadata."""

    id: str
    document_type: DocumentType
    document_subtype: str
    document_type_confidence: float
    is_expired: bool
    risk_score: str = "low"
    processing_time_ms: int
    fields: list[ExtractedField]
    risk_flags: list[str] = []
    validation_warnings: list[str] = []


class SampleInfo(BaseModel):
    """Metadata for a pre-loaded sample document."""

    id: str
    name: str
    type: str
    description: str
    thumbnail_url: str | None = None

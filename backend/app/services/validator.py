"""Post-processing validation and confidence adjustment for extracted documents.

Runs deterministic checks on the LLM's extraction output: date format
validation, ID number sanity checks, expiration verification, missing
required field detection, and requires_review enforcement. Computes an
overall risk score from the adjusted confidence values and flags.
"""

from __future__ import annotations

import re
from datetime import date

from pydantic import BaseModel

from app.models.document import (
    DocumentType,
    ExtractedField,
    LLMExtractionResult,
    RiskScore,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REQUIRED_FIELDS: dict[str, set[str]] = {
    "government_id": {
        "full_name",
        "date_of_birth",
        "id_number",
        "issuing_authority",
        "issue_date",
        "expiration_date",
    },
    "proof_of_address": {
        "account_holder_name",
        "address",
        "issuing_company",
        "statement_date",
    },
    "income_verification": {
        "employee_name",
        "employer",
        "pay_period",
        "gross_pay",
        "net_pay",
    },
}

DATE_FIELDS: set[str] = {
    "date_of_birth",
    "issue_date",
    "expiration_date",
    "statement_date",
}

_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
_MIN_ID_LENGTH = 5
_REVIEW_THRESHOLD = 0.80
_DATE_PENALTY = 0.15
_ID_PENALTY = 0.20


# ---------------------------------------------------------------------------
# Public result model
# ---------------------------------------------------------------------------


class ValidationResult(BaseModel):
    """Output of the validation pass — consumed by the route handler."""

    fields: list[ExtractedField]
    risk_score: RiskScore
    risk_flags: list[str]
    validation_warnings: list[str]
    is_expired: bool


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def validate_extraction(result: LLMExtractionResult) -> ValidationResult:
    """Run all post-processing validations on an LLM extraction result.

    Returns a ValidationResult with adjusted fields, computed risk score,
    updated risk flags, and validation warnings. The original result is
    never mutated.
    """
    warnings: list[str] = []
    risk_flags = list(result.risk_flags)

    # Per-field validation (rules 1-4)
    adjusted_fields: list[ExtractedField] = []
    for field in result.fields:
        f = _fix_null_confidence(field)
        f = _check_date_format(f, warnings)
        f = _check_id_number(f, warnings)
        f = _enforce_requires_review(f)
        adjusted_fields.append(f)

    # Cross-field checks (rules 5-6)
    is_expired = _check_expiration(adjusted_fields, result.is_expired, risk_flags, warnings)
    _check_missing_required(adjusted_fields, result.document_type, warnings)

    # Compute aggregate risk score
    risk_score = compute_risk_score(adjusted_fields, is_expired, risk_flags, result.document_type)

    return ValidationResult(
        fields=adjusted_fields,
        risk_score=risk_score,
        risk_flags=risk_flags,
        validation_warnings=warnings,
        is_expired=is_expired,
    )


# ---------------------------------------------------------------------------
# Rule 1: Null value with nonzero confidence
# ---------------------------------------------------------------------------


def _fix_null_confidence(field: ExtractedField) -> ExtractedField:
    """Force confidence to 0.0 when value is absent."""
    if field.value is None and field.confidence > 0.0:
        return field.model_copy(update={"confidence": 0.0})
    return field


# ---------------------------------------------------------------------------
# Rule 2: Date format validation
# ---------------------------------------------------------------------------


def _check_date_format(field: ExtractedField, warnings: list[str]) -> ExtractedField:
    """Validate YYYY-MM-DD date fields. Reduce confidence by 0.15 on failure."""
    if field.field_name not in DATE_FIELDS or field.value is None:
        return field

    if not _is_valid_date(field.value):
        new_conf = max(0.0, field.confidence - _DATE_PENALTY)
        warnings.append(f"Field '{field.field_name}' has invalid date format: '{field.value}'")
        return field.model_copy(update={"confidence": new_conf})

    return field


def _is_valid_date(value: str) -> bool:
    """Return True if value is a valid YYYY-MM-DD calendar date."""
    if not _DATE_RE.fullmatch(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


# ---------------------------------------------------------------------------
# Rule 3: ID number format check
# ---------------------------------------------------------------------------


def _check_id_number(field: ExtractedField, warnings: list[str]) -> ExtractedField:
    """Basic sanity check on ID number fields. Reduce confidence by 0.20 on failure."""
    if field.field_name != "id_number" or field.value is None:
        return field

    if len(field.value.strip()) < _MIN_ID_LENGTH:
        new_conf = max(0.0, field.confidence - _ID_PENALTY)
        warnings.append(f"Field 'id_number' has unexpected format: '{field.value}'")
        return field.model_copy(update={"confidence": new_conf})

    return field


# ---------------------------------------------------------------------------
# Rule 4: Enforce requires_review threshold
# ---------------------------------------------------------------------------


def _enforce_requires_review(field: ExtractedField) -> ExtractedField:
    """Set requires_review based on the 0.80 confidence threshold."""
    should_review = field.confidence < _REVIEW_THRESHOLD
    if field.requires_review != should_review:
        return field.model_copy(update={"requires_review": should_review})
    return field


# ---------------------------------------------------------------------------
# Rule 5: Server-side expiration check
# ---------------------------------------------------------------------------


def _check_expiration(
    fields: list[ExtractedField],
    llm_is_expired: bool,
    risk_flags: list[str],
    warnings: list[str],
) -> bool:
    """Verify expiration server-side. Returns the corrected is_expired value."""
    exp_field = next((f for f in fields if f.field_name == "expiration_date"), None)

    if exp_field is None or exp_field.value is None:
        return llm_is_expired

    if not _is_valid_date(exp_field.value):
        warnings.append(f"Cannot verify expiration: unparseable date '{exp_field.value}'")
        return llm_is_expired

    expired = date.fromisoformat(exp_field.value) < date.today()

    if expired and not llm_is_expired:
        if "document_expired" not in risk_flags:
            risk_flags.append("document_expired")
        warnings.append("Document appears expired (server-side check)")
        return True

    if not expired and llm_is_expired:
        warnings.append("LLM flagged document as expired but expiration date is in the future")
        return False

    return llm_is_expired


# ---------------------------------------------------------------------------
# Rule 6: Missing required fields
# ---------------------------------------------------------------------------


def _check_missing_required(
    fields: list[ExtractedField],
    document_type: DocumentType,
    warnings: list[str],
) -> set[str]:
    """Return set of missing required field names and add warnings."""
    required = REQUIRED_FIELDS.get(document_type, set())
    present = {f.field_name for f in fields if f.value is not None}
    missing = required - present

    for name in sorted(missing):
        warnings.append(f"Required field '{name}' is missing")

    return missing


# ---------------------------------------------------------------------------
# Risk scoring
# ---------------------------------------------------------------------------


def compute_risk_score(
    fields: list[ExtractedField],
    is_expired: bool,
    risk_flags: list[str],
    document_type: DocumentType,
) -> RiskScore:
    """Compute overall risk score from validated fields and flags.

    PRD §5 rules (waterfall — first match wins):
    - High: any field < 0.70, expired, or missing required fields
    - Medium: any field 0.70 <= conf < 0.90
    - Low: all fields >= 0.90
    """
    # Check for missing required fields
    required = REQUIRED_FIELDS.get(document_type, set())
    present = {f.field_name for f in fields if f.value is not None}
    if required - present:
        return "high"

    if is_expired:
        return "high"

    valued_fields = [f for f in fields if f.value is not None]

    if any(f.confidence < 0.70 for f in valued_fields):
        return "high"

    # >= 0.90 is "low" (see plan: boundary clarification)
    if any(0.70 <= f.confidence < 0.90 for f in valued_fields):
        return "medium"

    return "low"

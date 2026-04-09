"""Unit tests for the post-processing validation service.

Pure functions, no API calls, fast. Hand-crafted ExtractedField and
LLMExtractionResult instances test all 6 validation rules, risk scoring
boundaries, and edge cases.
"""

from app.models.document import ExtractedField, LLMExtractionResult
from app.services.validator import compute_risk_score, validate_extraction


def _field(
    name: str = "full_name",
    label: str = "Full Name",
    value: str | None = "Jordan Taylor",
    confidence: float = 0.95,
    requires_review: bool = False,
) -> ExtractedField:
    """Helper to build ExtractedField instances with defaults."""
    return ExtractedField(
        field_name=name,
        label=label,
        value=value,
        confidence=confidence,
        source_text=value,
        requires_review=requires_review,
    )


def _result(
    fields: list[ExtractedField] | None = None,
    document_type: str = "government_id",
    is_expired: bool = False,
    risk_flags: list[str] | None = None,
) -> LLMExtractionResult:
    """Helper to build LLMExtractionResult instances."""
    return LLMExtractionResult(
        document_type=document_type,  # type: ignore[arg-type]
        document_subtype="passport",
        document_type_confidence=0.99,
        is_expired=is_expired,
        fields=fields or [],
        risk_flags=risk_flags or [],
    )


# ---------------------------------------------------------------------------
# Rule 1: Null value with nonzero confidence
# ---------------------------------------------------------------------------


class TestNullValueConfidence:
    def test_null_value_forces_zero_confidence(self) -> None:
        r = _result(fields=[_field(value=None, confidence=0.85)])
        v = validate_extraction(r)
        assert v.fields[0].confidence == 0.0

    def test_present_value_keeps_confidence(self) -> None:
        r = _result(fields=[_field(value="Jordan", confidence=0.95)])
        v = validate_extraction(r)
        assert v.fields[0].confidence == 0.95


# ---------------------------------------------------------------------------
# Rule 2: Date format validation
# ---------------------------------------------------------------------------


class TestDateFormat:
    def test_valid_date_no_penalty(self) -> None:
        r = _result(fields=[_field(name="date_of_birth", value="1994-03-22")])
        v = validate_extraction(r)
        assert v.fields[0].confidence == 0.95
        assert not any("date_of_birth" in w for w in v.validation_warnings)

    def test_invalid_format_reduces_confidence(self) -> None:
        r = _result(fields=[_field(name="date_of_birth", value="03/22/1994", confidence=0.92)])
        v = validate_extraction(r)
        assert v.fields[0].confidence == 0.92 - 0.15
        assert any("date_of_birth" in w for w in v.validation_warnings)

    def test_invalid_calendar_date_reduces_confidence(self) -> None:
        r = _result(fields=[_field(name="date_of_birth", value="2024-02-30", confidence=0.90)])
        v = validate_extraction(r)
        assert v.fields[0].confidence == 0.90 - 0.15
        assert any("date_of_birth" in w for w in v.validation_warnings)

    def test_null_date_skipped(self) -> None:
        r = _result(fields=[_field(name="date_of_birth", value=None, confidence=0.0)])
        v = validate_extraction(r)
        # No date *format* warning — "missing" warnings are expected separately
        assert not any("invalid date format" in w.lower() for w in v.validation_warnings)

    def test_non_date_field_not_checked(self) -> None:
        r = _result(fields=[_field(name="full_name", value="not-a-date")])
        v = validate_extraction(r)
        assert v.fields[0].confidence == 0.95


# ---------------------------------------------------------------------------
# Rule 3: ID number format check
# ---------------------------------------------------------------------------


class TestIdNumber:
    def test_valid_id_no_penalty(self) -> None:
        r = _result(fields=[_field(name="id_number", value="P-6129480")])
        v = validate_extraction(r)
        assert v.fields[0].confidence == 0.95

    def test_short_id_reduces_confidence(self) -> None:
        r = _result(fields=[_field(name="id_number", value="123", confidence=0.90)])
        v = validate_extraction(r)
        assert v.fields[0].confidence == 0.90 - 0.20
        assert any("id_number" in w for w in v.validation_warnings)

    def test_empty_id_reduces_confidence(self) -> None:
        r = _result(fields=[_field(name="id_number", value="", confidence=0.85)])
        v = validate_extraction(r)
        assert v.fields[0].confidence == 0.85 - 0.20


# ---------------------------------------------------------------------------
# Rule 4: requires_review enforcement
# ---------------------------------------------------------------------------


class TestRequiresReview:
    def test_low_confidence_sets_review_true(self) -> None:
        r = _result(fields=[_field(confidence=0.75, requires_review=False)])
        v = validate_extraction(r)
        assert v.fields[0].requires_review is True

    def test_high_confidence_sets_review_false(self) -> None:
        r = _result(fields=[_field(confidence=0.85, requires_review=True)])
        v = validate_extraction(r)
        assert v.fields[0].requires_review is False

    def test_exactly_080_is_not_flagged(self) -> None:
        """Threshold is 'below 0.80', so 0.80 exactly is NOT flagged."""
        r = _result(fields=[_field(confidence=0.80)])
        v = validate_extraction(r)
        assert v.fields[0].requires_review is False


# ---------------------------------------------------------------------------
# Rule 5: Server-side expiration check
# ---------------------------------------------------------------------------


class TestExpiration:
    def test_past_date_corrects_is_expired(self) -> None:
        r = _result(
            fields=[_field(name="expiration_date", value="2020-01-01")],
            is_expired=False,
        )
        v = validate_extraction(r)
        assert v.is_expired is True
        assert "document_expired" in v.risk_flags
        assert any("expired" in w.lower() for w in v.validation_warnings)

    def test_future_date_corrects_false_positive(self) -> None:
        r = _result(
            fields=[_field(name="expiration_date", value="2035-12-31")],
            is_expired=True,
        )
        v = validate_extraction(r)
        assert v.is_expired is False
        assert any("future" in w.lower() for w in v.validation_warnings)

    def test_unparseable_date_falls_back_to_llm(self) -> None:
        r = _result(
            fields=[_field(name="expiration_date", value="not-a-date", confidence=0.5)],
            is_expired=True,
        )
        v = validate_extraction(r)
        assert v.is_expired is True  # Falls back to LLM's assessment
        has_date_warning = any(
            "unparseable" in w.lower() or "invalid date" in w.lower() for w in v.validation_warnings
        )
        assert has_date_warning

    def test_agreement_no_correction(self) -> None:
        r = _result(
            fields=[_field(name="expiration_date", value="2035-12-31")],
            is_expired=False,
        )
        v = validate_extraction(r)
        assert v.is_expired is False


# ---------------------------------------------------------------------------
# Rule 6: Missing required fields
# ---------------------------------------------------------------------------


class TestMissingRequired:
    def test_all_present_no_warning(self) -> None:
        fields = [
            _field(name="full_name"),
            _field(name="date_of_birth", value="1994-03-22"),
            _field(name="id_number", value="P-6129480"),
            _field(name="issuing_authority", value="USA"),
            _field(name="issue_date", value="2023-06-10"),
            _field(name="expiration_date", value="2033-06-09"),
        ]
        r = _result(fields=fields)
        v = validate_extraction(r)
        assert not any("missing" in w.lower() for w in v.validation_warnings)

    def test_missing_field_warns(self) -> None:
        r = _result(fields=[_field(name="full_name")])
        v = validate_extraction(r)
        missing_warnings = [w for w in v.validation_warnings if "missing" in w.lower()]
        assert len(missing_warnings) > 0

    def test_null_value_counts_as_missing(self) -> None:
        fields = [_field(name="full_name", value=None, confidence=0.0)]
        r = _result(fields=fields)
        v = validate_extraction(r)
        # full_name has null value, so other required fields are missing too
        missing_warnings = [w for w in v.validation_warnings if "missing" in w.lower()]
        assert len(missing_warnings) >= 1


# ---------------------------------------------------------------------------
# Confidence clamping
# ---------------------------------------------------------------------------


class TestConfidenceClamping:
    def test_date_penalty_clamps_to_zero(self) -> None:
        r = _result(fields=[_field(name="date_of_birth", value="bad-date", confidence=0.10)])
        v = validate_extraction(r)
        assert v.fields[0].confidence == 0.0

    def test_id_penalty_clamps_to_zero(self) -> None:
        r = _result(fields=[_field(name="id_number", value="AB", confidence=0.15)])
        v = validate_extraction(r)
        assert v.fields[0].confidence == 0.0


# ---------------------------------------------------------------------------
# Risk scoring
# ---------------------------------------------------------------------------


def _income_fields(override_conf: float | None = None, **overrides: float) -> list[ExtractedField]:
    """Build a complete set of required income_verification fields.

    All fields default to 0.95 confidence unless override_conf is set globally
    or individual field names are passed as kwargs (e.g., gross_pay=0.70).
    """
    base_conf = override_conf if override_conf is not None else 0.95
    names = ["employee_name", "employer", "pay_period", "gross_pay", "net_pay"]
    return [_field(name=n, value=f"val_{n}", confidence=overrides.get(n, base_conf)) for n in names]


class TestRiskScoring:
    def test_all_high_confidence_is_low_risk(self) -> None:
        fields = _income_fields(override_conf=0.95)
        assert compute_risk_score(fields, False, [], "income_verification") == "low"

    def test_one_medium_confidence_is_medium_risk(self) -> None:
        fields = _income_fields(gross_pay=0.85)
        assert compute_risk_score(fields, False, [], "income_verification") == "medium"

    def test_one_low_confidence_is_high_risk(self) -> None:
        fields = _income_fields(gross_pay=0.65)
        assert compute_risk_score(fields, False, [], "income_verification") == "high"

    def test_expired_is_high_risk(self) -> None:
        fields = _income_fields()
        assert compute_risk_score(fields, True, [], "income_verification") == "high"

    def test_missing_required_is_high_risk(self) -> None:
        # Only employee_name present, 4 required fields missing
        fields = [_field(name="employee_name", confidence=0.95)]
        assert compute_risk_score(fields, False, [], "income_verification") == "high"

    def test_boundary_090_is_low(self) -> None:
        """0.90 exactly is >= 0.90, so it's low risk."""
        fields = _income_fields(override_conf=0.90)
        assert compute_risk_score(fields, False, [], "income_verification") == "low"

    def test_boundary_070_is_medium(self) -> None:
        """0.70 exactly is >= 0.70 and < 0.90, so it's medium."""
        fields = _income_fields(override_conf=0.70)
        assert compute_risk_score(fields, False, [], "income_verification") == "medium"

    def test_boundary_0699_is_high(self) -> None:
        fields = _income_fields(override_conf=0.699)
        assert compute_risk_score(fields, False, [], "income_verification") == "high"

    def test_empty_fields_with_required_is_high(self) -> None:
        assert compute_risk_score([], False, [], "government_id") == "high"


# ---------------------------------------------------------------------------
# End-to-end validate_extraction
# ---------------------------------------------------------------------------


class TestValidateExtractionE2E:
    def test_clean_government_id_low_risk(self) -> None:
        fields = [
            _field(name="full_name", value="Jordan Taylor", confidence=0.99),
            _field(name="date_of_birth", value="1994-03-22", confidence=0.99),
            _field(name="id_number", value="P-6129480", confidence=0.99),
            _field(name="issuing_authority", value="USA", confidence=0.99),
            _field(name="issue_date", value="2023-06-10", confidence=0.99),
            _field(name="expiration_date", value="2033-06-09", confidence=0.99),
        ]
        r = _result(fields=fields)
        v = validate_extraction(r)
        assert v.risk_score == "low"
        assert v.is_expired is False
        assert all(not f.requires_review for f in v.fields)

    def test_bad_date_degrades_risk(self) -> None:
        fields = [
            _field(name="full_name", confidence=0.95),
            _field(name="date_of_birth", value="March 22, 1994", confidence=0.92),
            _field(name="id_number", value="P-6129480", confidence=0.95),
            _field(name="issuing_authority", value="USA", confidence=0.95),
            _field(name="issue_date", value="2023-06-10", confidence=0.95),
            _field(name="expiration_date", value="2033-06-09", confidence=0.95),
        ]
        r = _result(fields=fields)
        v = validate_extraction(r)
        # 0.92 - 0.15 = 0.77, which is medium range
        dob = next(f for f in v.fields if f.field_name == "date_of_birth")
        assert dob.confidence == 0.92 - 0.15
        assert dob.requires_review is True
        assert v.risk_score == "medium"
        assert any("date_of_birth" in w for w in v.validation_warnings)

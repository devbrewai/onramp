"""Integration tests for POST /api/process.

These tests hit the real Claude API and require ANTHROPIC_API_KEY in the
environment. Run them explicitly with: uv run pytest -m integration -v
"""

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app

client = TestClient(app)

needs_api_key = pytest.mark.skipif(
    not settings.anthropic_api_key,
    reason="ANTHROPIC_API_KEY not set (check backend/.env)",
)


def _assert_validation_invariants(body: dict[str, object]) -> None:
    """Assert structural invariants that must hold after validation."""
    assert body["risk_score"] in ("low", "medium", "high")
    assert isinstance(body["validation_warnings"], list)
    assert isinstance(body["risk_flags"], list)

    fields = body["fields"]
    assert isinstance(fields, list)
    for field in fields:
        assert isinstance(field, dict)
        conf = field["confidence"]
        assert 0.0 <= conf <= 1.0
        # requires_review must be consistent with the 0.80 threshold
        if conf < 0.80:
            assert field["requires_review"] is True, (
                f"Field '{field['field_name']}' has confidence {conf} but requires_review is False"
            )
        if conf >= 0.80:
            assert field["requires_review"] is False, (
                f"Field '{field['field_name']}' has confidence {conf} but requires_review is True"
            )


@pytest.mark.integration
@needs_api_key
def test_process_sample_passport() -> None:
    response = client.post("/api/process", data={"sample_id": "sample_passport"})
    assert response.status_code == 200
    body = response.json()

    assert body["document_type"] == "government_id"
    assert "passport" in body["document_subtype"].lower()
    assert body["processing_time_ms"] > 0
    assert body["id"]

    field_names = {f["field_name"] for f in body["fields"]}
    assert "full_name" in field_names
    assert "date_of_birth" in field_names
    assert "id_number" in field_names
    assert "expiration_date" in field_names

    _assert_validation_invariants(body)


@pytest.mark.integration
@needs_api_key
def test_process_sample_utility_bill() -> None:
    response = client.post("/api/process", data={"sample_id": "sample_utility_bill"})
    assert response.status_code == 200
    body = response.json()

    assert body["document_type"] == "proof_of_address"
    assert body["processing_time_ms"] > 0

    field_names = {f["field_name"] for f in body["fields"]}
    assert "account_holder_name" in field_names
    assert "address" in field_names
    assert "statement_date" in field_names

    _assert_validation_invariants(body)


@pytest.mark.integration
@needs_api_key
def test_process_sample_pay_stub() -> None:
    response = client.post("/api/process", data={"sample_id": "sample_pay_stub"})
    assert response.status_code == 200
    body = response.json()

    assert body["document_type"] == "income_verification"
    assert body["processing_time_ms"] > 0

    field_names = {f["field_name"] for f in body["fields"]}
    assert "employee_name" in field_names
    assert "employer" in field_names
    assert "gross_pay" in field_names
    assert "net_pay" in field_names

    _assert_validation_invariants(body)


def test_process_invalid_sample_id() -> None:
    response = client.post("/api/process", data={"sample_id": "nonexistent"})
    assert response.status_code == 404


def test_process_no_input() -> None:
    response = client.post("/api/process")
    assert response.status_code == 400

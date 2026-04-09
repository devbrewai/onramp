"""LLM-powered document classification and field extraction via Pydantic AI."""

from __future__ import annotations

from pydantic_ai import Agent, BinaryContent

from app.config import settings
from app.models.document import LLMExtractionResult

EXTRACTION_PROMPT = """\
You are a document processing AI for Onramp, a fintech onboarding platform.
Analyze the uploaded document image and extract structured data for identity
verification.

TASK:
1. Classify the document type: government_id, proof_of_address, or
   income_verification.
2. Determine the document subtype (e.g., "passport", "drivers_license",
   "utility_bill", "bank_statement", "pay_stub", "employment_letter").
3. Extract all relevant fields based on the document type.
4. For each field, provide:
   - field_name: a snake_case identifier
   - label: a human-readable label
   - value: the extracted value (null if not found)
   - confidence: 0.0 to 1.0 confidence score
   - source_text: the exact text in the document this was extracted from
   - requires_review: true if confidence < 0.80

DOCUMENT TYPE SCHEMAS:

government_id (passport, drivers_license):
  Required: full_name, date_of_birth, id_number, document_subtype,
            issuing_authority, issue_date, expiration_date
  Optional: nationality, gender, address, mrz_code, place_of_birth

proof_of_address (utility_bill, bank_statement, official_letter):
  Required: account_holder_name, address, document_subtype,
            issuing_company, statement_date
  Optional: account_number, amount_due

income_verification (pay_stub, employment_letter, tax_document):
  Required: employee_name, employer, pay_period, gross_pay, net_pay
  Optional: pay_frequency, ytd_gross, deductions, position_title

CONFIDENCE CALIBRATION:
- Field clearly visible and unambiguous: 0.92-0.99
- Field requires inference (e.g., address parsing): 0.75-0.90
- Field partially obscured or ambiguous: 0.50-0.75
- Field not found but might exist: 0.0-0.30

RULES:
- If a field is not present in the document, set value to null and
  confidence to 0.0.
- If a field is partially legible or ambiguous, extract your best guess
  and set confidence between 0.50-0.80.
- Format all dates as YYYY-MM-DD.
- Set is_expired to true if the document has an expiration date in the past.
- Add relevant risk_flags (e.g., "document_expired", "low_image_quality",
  "possible_alteration") when appropriate.
- Return valid structured data only.
"""

_agent: Agent[None, LLMExtractionResult] | None = None


def _get_agent() -> Agent[None, LLMExtractionResult]:
    """Lazily create the Pydantic AI agent so import works without an API key."""
    global _agent  # noqa: PLW0603
    if _agent is None:
        _agent = Agent(
            settings.llm_model,
            output_type=LLMExtractionResult,
            instructions=EXTRACTION_PROMPT,
        )
    return _agent


async def extract_document(image_bytes: bytes) -> LLMExtractionResult:
    """Send a document image to the LLM and get structured extraction results."""
    agent = _get_agent()
    result = await agent.run(
        [
            "Analyze this document and extract structured data for identity verification.",
            BinaryContent(data=image_bytes, media_type="image/png"),
        ]
    )
    return result.output

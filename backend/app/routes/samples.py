"""GET /api/samples — list available sample documents."""

from fastapi import APIRouter

from app.models.document import SampleInfo

router = APIRouter()

SAMPLES: list[SampleInfo] = [
    SampleInfo(
        id="sample_passport",
        name="Sample Passport",
        type="Government ID",
        description="US passport for identity verification",
    ),
    SampleInfo(
        id="sample_utility_bill",
        name="Sample Utility Bill",
        type="Proof of Address",
        description="Utility bill for address verification",
    ),
    SampleInfo(
        id="sample_pay_stub",
        name="Sample Pay Stub",
        type="Income Verification",
        description="Pay stub for income verification",
    ),
]


@router.get("/samples", response_model=list[SampleInfo])
def list_samples() -> list[SampleInfo]:
    """Return metadata for all available sample documents."""
    return SAMPLES

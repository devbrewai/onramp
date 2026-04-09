from pathlib import Path

import pytest
from PIL import Image

from app.services.converter import to_images

SAMPLES_DIR = Path(__file__).resolve().parent.parent / "data" / "samples"


def test_png_passthrough() -> None:
    png_bytes = (SAMPLES_DIR / "sample_passport.png").read_bytes()
    result = to_images(png_bytes, "image/png")
    assert len(result) == 1
    # Verify it's valid PNG (starts with PNG magic bytes)
    assert result[0][:8] == b"\x89PNG\r\n\x1a\n"


def test_jpeg_converted_to_png() -> None:
    # Create a tiny JPEG in memory
    import io

    buf = io.BytesIO()
    img = Image.new("RGB", (10, 10), color="red")
    img.save(buf, format="JPEG")
    jpeg_bytes = buf.getvalue()

    result = to_images(jpeg_bytes, "image/jpeg")
    assert len(result) == 1
    assert result[0][:8] == b"\x89PNG\r\n\x1a\n"


def test_pdf_to_images() -> None:
    pdf_bytes = (SAMPLES_DIR / "sample_utility_bill.pdf").read_bytes()
    result = to_images(pdf_bytes, "application/pdf")
    assert len(result) == 1  # Single-page PDF
    assert result[0][:8] == b"\x89PNG\r\n\x1a\n"


def test_unsupported_content_type() -> None:
    with pytest.raises(ValueError, match="Unsupported content type"):
        to_images(b"not a real file", "text/plain")

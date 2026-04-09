"""Generate the 3 sample documents for the Onramp demo.

All data is fictional using the Jordan Taylor persona.
Run from the backend directory: `uv run python scripts/generate_samples.py`
"""

from pathlib import Path

from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "samples"


# ---------------------------------------------------------------------------
# Shared persona
# ---------------------------------------------------------------------------
PERSONA = {
    "full_name": "Jordan Michael Taylor",
    "short_name": "Jordan Taylor",
    "display_name": "Jordan M. Taylor",
    "dob": "1994-03-22",
    "id_number": "P-6129480",
    "nationality": "American",
    "gender": "M",
    "issued": "2023-06-10",
    "expires": "2033-06-09",
    "address": "742 Elm Street, Austin, TX 78702",
    "employer": "TechCo Inc",
    "title": "Senior Software Engineer",
}


# ---------------------------------------------------------------------------
# 1. Sample Passport (PNG)
# ---------------------------------------------------------------------------
def generate_passport() -> None:
    width, height = 800, 560
    img = Image.new("RGB", (width, height), color=(0, 78, 100))
    draw = ImageDraw.Draw(img)

    # Use default font (monospace-ish, always available)
    font_large: ImageFont.FreeTypeFont | ImageFont.ImageFont
    font_medium: ImageFont.FreeTypeFont | ImageFont.ImageFont
    font_small: ImageFont.FreeTypeFont | ImageFont.ImageFont
    try:
        font_large = ImageFont.truetype("Helvetica", 24)
        font_medium = ImageFont.truetype("Helvetica", 16)
        font_small = ImageFont.truetype("Helvetica", 12)
    except OSError:
        font_large = ImageFont.load_default(size=24)
        font_medium = ImageFont.load_default(size=16)
        font_small = ImageFont.load_default(size=12)

    # Header
    draw.text((30, 20), "UNITED STATES OF AMERICA", fill="white", font=font_medium)
    draw.text((30, 45), "PASSPORT", fill=(200, 200, 200), font=font_large)

    # Photo placeholder
    draw.rectangle([(30, 100), (200, 310)], fill=(60, 60, 80), outline="white", width=2)
    draw.text((75, 195), "PHOTO", fill=(150, 150, 170), font=font_medium)

    # Fields
    fields = [
        ("Surname", "TAYLOR"),
        ("Given Names", "JORDAN MICHAEL"),
        ("Nationality", PERSONA["nationality"].upper()),
        ("Date of Birth", PERSONA["dob"]),
        ("Sex", PERSONA["gender"]),
        ("Place of Birth", "AUSTIN, TEXAS, U.S.A."),
        ("Date of Issue", PERSONA["issued"]),
        ("Date of Expiration", PERSONA["expires"]),
        ("Passport No.", PERSONA["id_number"]),
    ]

    y = 100
    for label, value in fields:
        draw.text((230, y), label, fill=(180, 200, 210), font=font_small)
        draw.text((230, y + 14), value, fill="white", font=font_medium)
        y += 40

    # MRZ zone
    mrz_y = height - 90
    draw.rectangle([(0, mrz_y - 5), (width, height)], fill=(0, 50, 65))
    mrz_line_1 = "P<USATAYLOR<<JORDAN<MICHAEL<<<<<<<<<<<<<<<<<<<<"
    mrz_line_2 = "P612948003USA9403225M3306091<<<<<<<<<<<<<<<<<06"
    draw.text((20, mrz_y), mrz_line_1, fill=(200, 220, 230), font=font_small)
    draw.text((20, mrz_y + 25), mrz_line_2, fill=(200, 220, 230), font=font_small)

    # SPECIMEN watermark
    watermark = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    wd = ImageDraw.Draw(watermark)
    wm_font: ImageFont.FreeTypeFont | ImageFont.ImageFont
    try:
        wm_font = ImageFont.truetype("Helvetica", 72)
    except OSError:
        wm_font = ImageFont.load_default(size=72)
    wd.text(
        (width // 2, height // 2),
        "SPECIMEN",
        fill=(255, 255, 255, 60),
        font=wm_font,
        anchor="mm",
    )
    watermark = watermark.rotate(30, expand=False, center=(width // 2, height // 2))

    img.paste(watermark, mask=watermark)
    img.save(OUTPUT_DIR / "sample_passport.png")
    print(f"  Created {OUTPUT_DIR / 'sample_passport.png'}")


# ---------------------------------------------------------------------------
# 2. Sample Utility Bill (PDF)
# ---------------------------------------------------------------------------
def generate_utility_bill() -> None:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)

    # Header
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 12, "Austin Energy", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, "721 Barton Springs Road, Austin, TX 78704", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Phone: (512) 494-9400  |  www.austinenergy.com", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    # Account info
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Monthly Billing Statement", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)

    info = [
        ("Account Holder", PERSONA["display_name"]),
        ("Service Address", PERSONA["address"]),
        ("Account Number", "****6129"),
        ("Statement Date", "February 15, 2026"),
        ("Due Date", "March 5, 2026"),
    ]
    for label, value in info:
        pdf.cell(60, 8, f"{label}:", new_x="RIGHT")
        pdf.cell(0, 8, value, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)

    # Charges table
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(100, 8, "Description", fill=True)
    pdf.cell(45, 8, "Amount", fill=True, align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 11)
    charges = [
        ("Electric Service (1,247 kWh)", "$98.42"),
        ("Fuel Adjustment", "$12.35"),
        ("Community Benefit Charge", "$8.60"),
        ("Regulatory Charge", "$5.23"),
        ("City of Austin Fee", "$3.00"),
        ("State Sales Tax", "$14.77"),
    ]
    for desc, amount in charges:
        pdf.cell(100, 7, desc)
        pdf.cell(45, 7, amount, align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(100, 8, "Total Amount Due")
    pdf.cell(45, 8, "$142.37", align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(12)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 6, "This is a sample document for demonstration purposes only.", new_x="LMARGIN")

    pdf.output(str(OUTPUT_DIR / "sample_utility_bill.pdf"))
    print(f"  Created {OUTPUT_DIR / 'sample_utility_bill.pdf'}")


# ---------------------------------------------------------------------------
# 3. Sample Pay Stub (PDF)
# ---------------------------------------------------------------------------
def generate_pay_stub() -> None:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)

    # Header
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "TechCo Inc", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    addr = "500 Congress Avenue, Suite 400, Austin, TX 78701"
    pdf.cell(0, 6, addr, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Employee Pay Statement", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)

    # Employee info
    emp_info = [
        ("Employee Name", PERSONA["short_name"]),
        ("Position", PERSONA["title"]),
        ("Employee ID", "EMP-2847"),
        ("Pay Period", "February 1 - February 28, 2026"),
        ("Pay Date", "February 28, 2026"),
        ("Pay Frequency", "Monthly"),
    ]
    for label, value in emp_info:
        pdf.cell(55, 7, f"{label}:", new_x="RIGHT")
        pdf.cell(0, 7, value, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)

    # Earnings
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Earnings", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(70, 7, "Description", fill=True)
    pdf.cell(35, 7, "Hours", fill=True, align="R")
    pdf.cell(35, 7, "Rate", fill=True, align="R")
    pdf.cell(40, 7, "Amount", fill=True, align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(70, 7, "Regular Salary")
    pdf.cell(35, 7, "N/A", align="R")
    pdf.cell(35, 7, "N/A", align="R")
    pdf.cell(40, 7, "$13,750.00", align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(140, 7, "Gross Pay")
    pdf.cell(40, 7, "$13,750.00", align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)

    # Deductions
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Deductions", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(140, 7, "Description", fill=True)
    pdf.cell(40, 7, "Amount", fill=True, align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 10)
    deductions = [
        ("Federal Income Tax", "$2,062.50"),
        ("State Income Tax (TX)", "$0.00"),
        ("Social Security (FICA)", "$852.50"),
        ("Medicare", "$199.38"),
        ("401(k) Contribution (6%)", "$825.00"),
        ("Health Insurance - Medical", "$185.00"),
        ("Health Insurance - Dental", "$42.00"),
        ("Health Insurance - Vision", "$18.00"),
    ]
    for desc, amount in deductions:
        pdf.cell(140, 7, desc)
        pdf.cell(40, 7, amount, align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(2)
    total_deductions = "$4,184.38"
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(140, 7, "Total Deductions")
    pdf.cell(40, 7, total_deductions, align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)

    # Summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Pay Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    summary = [
        ("Gross Pay", "$13,750.00"),
        ("Total Deductions", "-$4,184.38"),
        ("Net Pay", "$9,565.62"),
    ]
    for label, value in summary:
        pdf.cell(140, 7, label)
        pdf.cell(40, 7, value, align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(140, 8, "Year-to-Date Gross")
    pdf.cell(40, 8, "$27,500.00", align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 6, "This is a sample document for demonstration purposes only.", new_x="LMARGIN")

    pdf.output(str(OUTPUT_DIR / "sample_pay_stub.pdf"))
    print(f"  Created {OUTPUT_DIR / 'sample_pay_stub.pdf'}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating sample documents...")
    generate_passport()
    generate_utility_bill()
    generate_pay_stub()
    print("Done.")


if __name__ == "__main__":
    main()

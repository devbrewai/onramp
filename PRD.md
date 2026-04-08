# Product Requirements Document

# Demo 2: AI Document Intake for Fintech Onboarding

**Project:** Devbrew Portfolio Demo - "Onramp"
**Author:** Joe Kariuki, Founder
**Date:** March 20, 2026 (Revised)
**URL:** devbrew.ai/work/document-intake-agent
**Build Time:** 5 days (~5-6 hours/day, ~28 hours total)
**Status:** Not started

---

## 1. Purpose

This demo proves Devbrew can build intelligent document processing that replaces manual KYC and onboarding workflows. For fintech startups, onboarding is where users are won or lost. A 48-hour manual review means 40% of applicants drop off before they ever use the product. AI document processing cuts that to seconds.

The demo is embedded in a mock fintech onboarding platform called **Onramp**, not presented as a standalone OCR tool. Prospects should see a product feature that solves their onboarding bottleneck.

### What This Demo Sells

- Document AI for KYC and identity verification
- LLM-powered data extraction and validation
- Confidence scoring and human-in-the-loop review
- The pipeline: upload -> classify -> extract -> validate -> approve
- The dream outcome: "Onboarding that used to take 48 hours now takes 30 seconds. 40% dropout becomes 90% conversion."

### Target Viewer

Seed to Series A fintech startup founders whose products require identity verification, document collection, or onboarding flows. Neobanks processing KYC. Lending platforms verifying income documents. Payment companies onboarding merchants. Insurance startups processing applications. Any fintech founder whose users upload documents that someone currently reviews by hand.

---

## 2. Product Overview

### What the User Sees

A mock fintech onboarding and compliance platform called **Onramp**. Onramp helps fintech companies automate their user verification and onboarding. The UI includes:

- A dashboard showing onboarding pipeline statistics
- A document upload area (drag-and-drop)
- A processing pipeline view showing documents moving through verification stages
- An extraction results view with confidence scores and editable fields
- An applicant queue showing processed applications

### What the AI Does

1. **Accepts document uploads** (PDF, image, or simulated upload for demo)
2. **Classifies the document type** (government ID, proof of address, income verification)
3. **Extracts key fields** based on document type (e.g., ID: name, DOB, ID number, expiry)
4. **Validates extracted data** with confidence scores per field
5. **Flags low-confidence extractions** for human review
6. **Structures output** into a clean, editable applicant profile

---

## 3. Supported Document Types

Build extraction templates for 3 document types. Each type has predefined fields to extract. All framed around fintech onboarding use cases.

### Type 1: Government-Issued ID (Primary KYC Document)

This is the hero document type. Every fintech company needs to verify identity.

| Field | Example | Required |
| --- | --- | --- |
| Full Name | Alexander James Rivera | Yes |
| Date of Birth | 1992-07-14 | Yes |
| ID Number | P-8847291 | Yes |
| Document Type | Passport / Driver's License | Yes |
| Issuing Country/State | United States | Yes |
| Issue Date | 2022-03-20 | Yes |
| Expiration Date | 2032-03-19 | Yes |
| Nationality | American | No |
| Gender | M | No |
| Address (if on document) | 1847 Oak Street, Austin, TX 78701 | No |
| MRZ Code (passports) | P<USARIVERA<<ALEXANDER<JAMES... | No |

### Type 2: Proof of Address (Secondary KYC Document)

Utility bills, bank statements, or official letters used to verify residency.

| Field | Example | Required |
| --- | --- | --- |
| Account Holder Name | Alexander J. Rivera | Yes |
| Address | 1847 Oak Street, Austin, TX 78701 | Yes |
| Document Type | Utility Bill / Bank Statement / Official Letter | Yes |
| Issuing Company | Austin Energy | Yes |
| Statement Date | 2026-02-15 | Yes |
| Account Number | ****8847 | No |
| Amount Due/Balance | $142.37 | No |

### Type 3: Income Verification (For Lending / Credit Products)

Pay stubs, employment letters, or tax documents used for income-based decisions.

| Field | Example | Required |
| --- | --- | --- |
| Employee Name | Alexander Rivera | Yes |
| Employer | TechCo Inc | Yes |
| Pay Period | Feb 1 - Feb 28, 2026 | Yes |
| Gross Pay | $13,750.00 | Yes |
| Net Pay | $9,847.23 | Yes |
| Pay Frequency | Monthly | No |
| YTD Gross | $27,500.00 | No |
| Deductions | Federal Tax, State Tax, 401k, Health Insurance | No |
| Position/Title | Senior Software Engineer | No |

---

## 4. User Flows

### Flow 1: Single Document Upload and Verification

```
1. User lands on Onramp dashboard
2. User drags a passport image into the upload area
   (or clicks to browse, or uses a pre-loaded sample document)
3. Upload animation plays (file icon moves to processing area)
4. Verification pipeline view activates:
   - Step 1: "Reading document..." (1-2 sec)
   - Step 2: "Classifying document type..." (1 sec)
   - Step 3: "Extracting identity fields..." (2-3 sec)
   - Step 4: "Validating data..." (1 sec)
5. Results view appears:
   - Document type badge: "Government ID - Passport"
   - Extracted fields in a form layout
   - Each field shows: label, extracted value, confidence score (%)
   - High confidence (>90%): green indicator, auto-approved
   - Medium confidence (70-90%): yellow indicator, needs review
   - Low confidence (<70%): red indicator, flagged for manual check
6. User can edit any field, then click "Approve" to finalize
7. Approved data appears in the applicant queue
```

### Flow 2: Pre-Loaded Sample Documents

Provide 3 pre-loaded sample documents:

- "Sample Passport" (a realistic mock passport image with SPECIMEN watermark)
- "Sample Utility Bill" (a mock utility bill PDF)
- "Sample Pay Stub" (a mock pay stub PDF)

**Clicking a sample triggers the same pipeline as a real upload.**

### Flow 3: Applicant Queue (Display Only)

Show a table of previously "verified" applicants to demonstrate production usage:

| Applicant | Documents | Status | Risk Score | Verified Date |
| --- | --- | --- | --- | --- |
| Alex Rivera | ID, Address | Approved | Low | Mar 15, 2026 |
| Sarah Chen | ID, Address, Income | Review Needed | Medium | Mar 14, 2026 |
| James Park | ID | Approved | Low | Mar 13, 2026 |
| Maria Santos | ID, Address | Flagged | High | Mar 12, 2026 |

This is mock/static data to fill the dashboard and make the product feel lived-in.

---

## 5. Technical Architecture

### System Diagram

```
[React + Vite Frontend (Vercel / Cloudflare Pages)]
    |
    |-- Mock Platform UI (dashboard, upload, results, applicant queue)
    |-- Document Upload Component
    |       |
    |       |-- File upload or sample document selection
    |       |-- Progress/pipeline visualization
    |       |-- Results display with confidence scores
    |       |
    [FastAPI Backend (Render)]
        |
        |-- /api/process (main document processing endpoint)
        |       |
        |       |-- Document Classifier
        |       |       |-- LLM-based classification (ID/address/income)
        |       |       |-- Returns document_type + confidence
        |       |
        |       |-- Field Extractor
        |       |       |-- LLM with structured output
        |       |       |-- Document type determines extraction schema
        |       |       |-- Returns fields + confidence per field
        |       |
        |       |-- Validator
        |       |       |-- Format checks (dates, ID numbers)
        |       |       |-- Expiration check (is the ID still valid?)
        |       |       |-- Cross-field validation (name consistency)
        |       |       |-- Risk scoring (based on confidence + flags)
        |       |
        |-- /api/samples (returns list of sample documents)
        |-- /api/health
```

### Tech Stack

| Component | Technology | Rationale |
| --- | --- | --- |
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui | SPA, consistent with Demo 1 |
| **Backend** | Python 3.11+, FastAPI | Best for document processing workloads |
| **LLM** | Anthropic Claude 3.5 Sonnet (primary) | Strong at structured extraction, handles vision |
| **OCR/Vision** | Claude Vision (for images) or pdf2image + Claude | Claude reads PDFs and images directly |
| **Document Parsing** | PyMuPDF (fitz) for PDF text extraction, Pillow for image handling | Free, reliable |
| **Deployment** | Vercel or Cloudflare Pages (frontend), Render (backend) | $0 cost |

### Key Architecture Decision: LLM-First, Not OCR-First

Use LLM vision directly:

1. Convert PDF pages to images (if needed)
2. Send images to Claude Vision with extraction prompt
3. Claude reads the document and extracts structured data in one pass

Simpler architecture, higher accuracy on varied layouts, and showcases modern AI approach.

### Extraction Prompt Structure

```
You are a document processing AI for Onramp, a fintech onboarding
platform. Analyze the uploaded document and extract structured data
for identity verification.

TASK:
1. Classify the document type: government_id, proof_of_address,
   or income_verification
2. Extract all relevant fields based on the document type
3. For each field, provide:
   - field_name: the field identifier
   - value: the extracted value
   - confidence: 0.0 to 1.0 confidence score
   - source_text: the exact text in the document this was extracted from

DOCUMENT TYPE SCHEMAS:
[Include the field schemas from Section 3 above]

ADDITIONAL VALIDATION:
- Check if government ID is expired
- Verify date formats are consistent
- Flag if name format seems unusual or potentially misspelled
- For MRZ codes, validate checksum digits if present

RULES:
- If a field is not present, set value to null and confidence to 0.0
- If a field is partially legible or ambiguous, extract best guess
  and set confidence between 0.5-0.8
- Dates should be formatted as YYYY-MM-DD
- Return valid JSON only

OUTPUT FORMAT:
{
  "document_type": "government_id",
  "document_subtype": "passport",
  "document_type_confidence": 0.98,
  "is_expired": false,
  "fields": [
    {
      "field_name": "full_name",
      "value": "Alexander James Rivera",
      "confidence": 0.99,
      "source_text": "RIVERA, ALEXANDER JAMES"
    },
    ...
  ],
  "risk_flags": [],
  "processing_time_ms": 2340
}
```

### Confidence Score Calibration

Apply these rules:

- Field clearly visible and unambiguous: 0.92-0.99
- Field requires inference (e.g., address parsing from unstructured text): 0.75-0.90
- Field partially obscured, low quality, or ambiguous: 0.50-0.75
- Field not found but might exist: 0.0-0.30

Post-processing validation adjustments:

- Date format valid? If not, reduce confidence by 0.15
- ID number matches expected format? If not, reduce by 0.20
- Document expired? Add risk flag
- Name on ID vs. name on address doc mismatch? Flag for review

### Risk Scoring

Assign an overall risk score to each applicant based on:

| Factor | Impact |
| --- | --- |
| All fields >90% confidence | Low risk |
| Any field 70-90% confidence | Medium risk |
| Any field <70% confidence | High risk |
| Expired document | High risk |
| Name mismatch across documents | High risk |
| Missing required fields | High risk |

---

## 6. Frontend Specification

### Mock Platform UI (Onramp Dashboard)

**Layout:**

- Top navigation bar: Logo ("Onramp"), Dashboard, Applicants, Documents, Settings, user avatar
- Main content: dashboard stats at top, upload area center, applicant queue below

**Dashboard Stats (mock/static):**

- Applicants Processed: 1,247
- Average Verification Time: 28 seconds
- Auto-Approval Rate: 78%
- Pending Review: 12

These stats tell the story: fast processing, high automation rate, minimal manual work.

**Upload Area:**

- Large drag-and-drop zone (dashed border, icon, "Drop documents here or browse")
- Below the drop zone: "Or try a sample:" with 3 clickable sample document cards
    - Each card shows document thumbnail, name, and type
- Accepted formats: PDF, PNG, JPG

**Verification Pipeline View:**
When a document is being processed:

```
[Upload] -> [Classify] -> [Extract] -> [Validate]
   check      check         loading      pending
```

Each stage shows icon, label, status, and time taken.

**Results View:**

- **Document Preview:** Thumbnail of original document (left panel, ~40%)
- **Extracted Data:** Form layout (right panel, ~60%)
    - Document Type badge (e.g., "Government ID - Passport" with green badge)
    - Each field: Label, Value (editable input), Confidence badge (green/yellow/red)
    - Fields flagged for review have yellow highlight
    - Risk score indicator at top (Low/Medium/High)
    - If document is expired, show red warning banner
- **Action Buttons:** "Approve" (primary), "Flag for Review" (secondary), "Re-process" (tertiary)

**Applicant Queue (below results):**

- Table with sortable columns
- Filter by status (Approved, Review Needed, Flagged)
- Risk score badge per applicant
- Documents received count

**Design:**

- Clean, professional fintech compliance aesthetic
- Light mode (contrast with Demo 1's dark mode)
- Accent color: emerald (signals "approved", "verified")
- Should look like a real compliance tool that a team uses daily

---

## 7. Backend Specification

### API Endpoints

**POST /api/process**

```
Request (multipart/form-data):
- file: PDF or image file
OR
- sample_id: "sample_passport" | "sample_utility_bill" | "sample_pay_stub"

Response:
{
  "id": "doc_abc123",
  "document_type": "government_id",
  "document_subtype": "passport",
  "document_type_confidence": 0.98,
  "is_expired": false,
  "risk_score": "low",
  "processing_time_ms": 2840,
  "fields": [
    {
      "field_name": "full_name",
      "label": "Full Name",
      "value": "Alexander James Rivera",
      "confidence": 0.99,
      "requires_review": false
    },
    {
      "field_name": "expiration_date",
      "label": "Expiration Date",
      "value": "2032-03-19",
      "confidence": 0.95,
      "requires_review": false
    },
    ...
  ],
  "risk_flags": [],
  "validation_warnings": []
}
```

**GET /api/samples**

```
Response:
{
  "samples": [
    {
      "id": "sample_passport",
      "name": "Sample Passport",
      "type": "Government ID",
      "description": "US passport for identity verification",
      "thumbnail_url": "/samples/passport_thumb.png"
    },
    {
      "id": "sample_utility_bill",
      "name": "Sample Utility Bill",
      "type": "Proof of Address",
      "description": "Utility bill for address verification",
      "thumbnail_url": "/samples/utility_thumb.png"
    },
    {
      "id": "sample_pay_stub",
      "name": "Sample Pay Stub",
      "type": "Income Verification",
      "description": "Pay stub for income verification",
      "thumbnail_url": "/samples/paystub_thumb.png"
    }
  ]
}
```

**GET /api/health**

```
Response: {"status": "ok", "version": "1.0.0"}
```

### Sample Documents

Create 3 realistic sample documents:

1. **Sample Passport:** Mock passport-style image with SPECIMEN watermark. Fictional data (Alex Rivera). Include MRZ code area.
2. **Sample Utility Bill:** Professional utility bill PDF. Fictional utility company, fictional address matching the passport.
3. **Sample Pay Stub:** Realistic pay stub PDF. Fictional employer, salary consistent with a tech professional.

**All sample documents use only fictional data. No real names, addresses, or ID numbers.**

---

## 8. Key Metrics to Display

Show on the /work/document-intake-agent project page:

| Metric | Value | Context |
| --- | --- | --- |
| **Processing time** | Under 30 seconds per document | vs. 24-48 hours manual review |
| **Auto-approval rate** | 78% of applicants | Approved without human intervention |
| **Extraction accuracy** | 96%+ | Field-level accuracy |
| **Human review rate** | ~15% of fields flagged | Only genuinely uncertain extractions need humans |

Frame with the outcome: "Onboarding that used to take 48 hours now takes 30 seconds. Your compliance team reviews exceptions, not everything."

---

## 9. Build Plan (5 Days)

### Day 1: Project Setup + Mock UI (~6 hours)

- [ ] Initialize React + Vite + TypeScript project with Tailwind + shadcn/ui
- [ ] Build Onramp mock dashboard layout
    - [ ] Top navigation bar
    - [ ] Dashboard stats cards (static data reflecting fintech onboarding metrics)
    - [ ] Document upload area with drag-and-drop
    - [ ] Sample document cards
    - [ ] Applicant queue table (static data)
- [ ] Create responsive layout (desktop + mobile)
- [ ] Set up FastAPI backend project

**Deliverable:** Static mock fintech onboarding platform UI.

### Day 2: Sample Documents + Backend Foundation (~6 hours)

- [ ] Create 3 sample documents
    - [ ] Design mock passport image
    - [ ] Create utility bill PDF
    - [ ] Create pay stub PDF
- [ ] Set up FastAPI endpoints
- [ ] Implement PDF-to-image conversion (PyMuPDF)
- [ ] Implement LLM extraction pipeline
    - [ ] Extraction prompt with KYC-specific structured output
    - [ ] Response parsing
- [ ] Test extraction on all 3 sample documents
- [ ] Iterate on extraction prompt for accuracy

**Deliverable:** Backend that extracts structured KYC data from documents.

### Day 3: Validation + Risk Scoring (~5 hours)

- [ ] Implement field validation rules
    - [ ] Date format validation
    - [ ] ID number format validation
    - [ ] Expiration date check
    - [ ] Cross-document name consistency
- [ ] Implement risk scoring logic
- [ ] Implement confidence adjustment
- [ ] Add review flagging (fields below 80% confidence)
- [ ] Create /api/process endpoint with full pipeline
- [ ] Test with all 3 document types

**Deliverable:** Validated extraction pipeline with risk scoring.

### Day 4: Frontend Integration + Results UI (~6 hours)

- [ ] Build verification pipeline animation (4-stage)
- [ ] Build results view
    - [ ] Document preview panel
    - [ ] Extracted fields form with confidence badges
    - [ ] Risk score indicator
    - [ ] Expired document warning
    - [ ] Editable fields with approve/flag states
- [ ] Integrate upload with backend
- [ ] Integrate sample document clicks
- [ ] Handle loading, error, and empty states
- [ ] Test all flows end-to-end

**Deliverable:** Fully integrated document verification demo.

### Day 5: Polish + Deploy (~5 hours)

- [ ] UI polish (animations, confidence badge colors, tooltips)
- [ ] Support user file uploads with disclaimer: "This is a demo. Do not upload real personal documents."
- [ ] Deploy frontend and backend
- [ ] End-to-end testing on deployed URLs
- [ ] Create /work/document-intake-agent page on devbrew.ai
    - [ ] Use outcome-led copy from site repositioning doc v2
    - [ ] Hero with screenshots
    - [ ] Problem / Solution / Impact / Technical Details
    - [ ] CTA
- [ ] Mobile testing

**Deliverable:** Deployed, polished demo.

---

## 10. Environment Variables

### Backend (.env)
```
ANTHROPIC_API_KEY=sk-ant-...
CORS_ORIGINS=https://devbrew.ai,http://localhost:3000
MAX_FILE_SIZE_MB=10
LOG_LEVEL=info
```

### Frontend (.env)
```
VITE_API_URL=https://document-intake-api.onrender.com
```

---

## 11. Success Criteria

The demo is DONE when:

- [ ] A fintech founder can visit the demo and process a sample document
- [ ] The Onramp UI looks like a real fintech compliance platform
- [ ] Processing a sample document takes <30 seconds end-to-end
- [ ] Extracted fields display with confidence scores and risk flags
- [ ] At least one field per document is flagged for review (shows human-in-the-loop)
- [ ] Users can edit extracted fields before approving
- [ ] The risk scoring feels credible and consistent
- [ ] Users can also upload their own documents (with disclaimer)
- [ ] Works on desktop and mobile

---

## 12. What NOT to Build

- User authentication
- Database persistence
- Batch upload (one document at a time)
- Real identity verification (no actual ID databases)
- Export functionality (button visible but non-functional)
- Multi-page document support beyond 3 pages
- Sanctions screening integration
- Liveness detection or selfie matching
- API documentation for the demo

---

## 13. Risk Mitigation

| Risk | Impact | Mitigation |
| --- | --- | --- |
| LLM API costs from user-uploaded documents | High | Rate limit: 10 documents per session |
| Users uploading real personal documents | High | Prominent disclaimer on upload screen. "DEMO ONLY. Do not upload real identity documents." |
| LLM extraction quality varies by document layout | Medium | Strong prompt engineering; pre-loaded samples are quality-controlled |
| Processing time too long (>30 sec) | Medium | Optimize prompt length; cache sample document results |

---

## 14. Future Enhancements (Do NOT Build Now)

Discuss with prospects:

- Multi-document applicant profiles (link ID + address + income for one person)
- Sanctions screening integration (connect to OFAC/EU lists)
- Liveness detection and selfie matching
- Batch processing for high-volume onboarding
- Webhook notifications on approval/rejection
- Integration with compliance platforms (Alloy, Persona, Sardine)
- Multi-language document support
- Audit trail and regulatory reporting
- Custom extraction templates per document type
- Risk model training on client-specific fraud patterns

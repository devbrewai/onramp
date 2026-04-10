// API response types mirroring backend Pydantic models.
// These are the frontend's source of truth for the network boundary.

export type DocumentType =
  | "government_id"
  | "proof_of_address"
  | "income_verification"

export type RiskScore = "low" | "medium" | "high"

export type ExtractedField = {
  field_name: string
  label: string
  value: string | null
  confidence: number
  source_text: string | null
  requires_review: boolean
}

export type ProcessResponse = {
  id: string
  document_type: DocumentType
  document_subtype: string
  document_type_confidence: number
  is_expired: boolean
  risk_score: RiskScore
  processing_time_ms: number
  fields: ExtractedField[]
  risk_flags: string[]
  validation_warnings: string[]
}

export type SampleInfo = {
  id: string
  name: string
  type: string
  description: string
  thumbnail_url: string | null
}

// Dashboard view state (discriminated union)
export type DashboardView =
  | { status: "idle" }
  | { status: "processing"; file: File | null; sampleId: string | null }
  | { status: "results"; result: ProcessResponse; previewUrl: string | null }
  | { status: "error"; message: string }

// Mock data for the static Onramp dashboard. All values are hardcoded
// fictional data — see PRD §3, §4, and §6 for the canonical definitions.
// Replaced with real backend data in Day 4 (DEV-110 milestone onward).

export type ApplicantStatus = "Approved" | "Review Needed" | "Flagged"
export type RiskLevel = "Low" | "Medium" | "High"
export type DocumentTag = "ID" | "Address" | "Income"

export type Applicant = {
  id: string
  name: string
  documents: DocumentTag[]
  status: ApplicantStatus
  risk: RiskLevel
  verifiedDate: string
}

export type SampleDocumentType =
  | "government_id"
  | "proof_of_address"
  | "income_verification"

export type SampleDocument = {
  id: string
  name: string
  type: SampleDocumentType
  typeLabel: string
  description: string
}

export type DashboardStats = {
  applicantsProcessed: number
  avgVerificationSeconds: number
  autoApprovalRate: number
  pendingReview: number
}

export const dashboardStats: DashboardStats = {
  applicantsProcessed: 1247,
  avgVerificationSeconds: 28,
  autoApprovalRate: 0.78,
  pendingReview: 12,
}

export const applicants: Applicant[] = [
  {
    id: "1",
    name: "Alex Rivera",
    documents: ["ID", "Address"],
    status: "Approved",
    risk: "Low",
    verifiedDate: "Mar 15, 2026",
  },
  {
    id: "2",
    name: "Sarah Chen",
    documents: ["ID", "Address", "Income"],
    status: "Review Needed",
    risk: "Medium",
    verifiedDate: "Mar 14, 2026",
  },
  {
    id: "3",
    name: "James Park",
    documents: ["ID"],
    status: "Approved",
    risk: "Low",
    verifiedDate: "Mar 13, 2026",
  },
  {
    id: "4",
    name: "Maria Santos",
    documents: ["ID", "Address"],
    status: "Flagged",
    risk: "High",
    verifiedDate: "Mar 12, 2026",
  },
]

export const sampleDocuments: SampleDocument[] = [
  {
    id: "sample_passport",
    name: "Sample Passport",
    type: "government_id",
    typeLabel: "Government ID",
    description: "US passport for identity verification",
  },
  {
    id: "sample_utility_bill",
    name: "Sample Utility Bill",
    type: "proof_of_address",
    typeLabel: "Proof of Address",
    description: "Utility bill for address verification",
  },
  {
    id: "sample_pay_stub",
    name: "Sample Pay Stub",
    type: "income_verification",
    typeLabel: "Income Verification",
    description: "Pay stub for income verification",
  },
]

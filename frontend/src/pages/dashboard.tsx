import { useCallback, useState } from "react"
import { AlertTriangle, RotateCcw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { ApplicantQueue } from "@/components/dashboard/applicant-queue"
import { ProcessingView } from "@/components/dashboard/processing-view"
import { ResultsView } from "@/components/dashboard/results-view"
import { SampleDocumentCards } from "@/components/dashboard/sample-document-cards"
import { StatsCards } from "@/components/dashboard/stats-cards"
import { UploadArea } from "@/components/dashboard/upload-area"
import {
  applicants as mockApplicants,
  type Applicant,
  type DocumentTag,
  type RiskLevel,
} from "@/lib/mock-data"
import {
  getSessionCount,
  incrementSessionCount,
  isSessionLimitReached,
  SESSION_LIMIT,
} from "@/lib/rate-limit"
import type {
  DashboardView,
  DocumentType,
  ExtractedField,
  ProcessResponse,
  RiskScore,
} from "@/lib/types"

const DOC_TAG_MAP: Record<DocumentType, DocumentTag> = {
  government_id: "ID",
  proof_of_address: "Address",
  income_verification: "Income",
}

const RISK_MAP: Record<RiskScore, RiskLevel> = {
  low: "Low",
  medium: "Medium",
  high: "High",
}

export function Dashboard() {
  const [view, setView] = useState<DashboardView>({ status: "idle" })
  const [allApplicants, setAllApplicants] =
    useState<Applicant[]>(mockApplicants)
  const [docsUsed, setDocsUsed] = useState(getSessionCount)

  const handleFileUpload = (file: File) => {
    if (isSessionLimitReached()) {
      setView({
        status: "error",
        message: `Session limit reached (${SESSION_LIMIT} documents). Refresh the page to start a new session.`,
      })
      return
    }
    setView({ status: "processing", file, sampleId: null })
  }

  const handleSampleClick = (sampleId: string) => {
    if (isSessionLimitReached()) {
      setView({
        status: "error",
        message: `Session limit reached (${SESSION_LIMIT} documents). Refresh the page to start a new session.`,
      })
      return
    }
    setView({ status: "processing", file: null, sampleId })
  }

  const handleComplete = useCallback(
    (result: ProcessResponse, previewUrl: string | null) => {
      setDocsUsed(incrementSessionCount())
      setView({ status: "results", result, previewUrl })
    },
    [],
  )

  const handleError = useCallback((message: string) => {
    setView({ status: "error", message })
  }, [])

  const handleApprove = (editedFields: ExtractedField[]) => {
    if (view.status !== "results") return
    const applicant = resultToApplicant(view.result, editedFields, "Approved")
    setAllApplicants((prev) => [applicant, ...prev])
    if (view.previewUrl) URL.revokeObjectURL(view.previewUrl)
    setView({ status: "idle" })
  }

  const handleFlagForReview = () => {
    if (view.status !== "results") return
    const applicant = resultToApplicant(
      view.result,
      view.result.fields,
      "Review Needed",
    )
    setAllApplicants((prev) => [applicant, ...prev])
    if (view.previewUrl) URL.revokeObjectURL(view.previewUrl)
    setView({ status: "idle" })
  }

  const handleNewDocument = () => {
    if (view.status === "results" && view.previewUrl) {
      URL.revokeObjectURL(view.previewUrl)
    }
    setView({ status: "idle" })
  }

  return (
    <main className="mx-auto max-w-7xl space-y-8 px-4 py-8 sm:px-6 lg:px-8">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-zinc-900">
          Onboarding Dashboard
        </h1>
        <p className="mt-1 text-sm text-zinc-500">
          Verify identity, address, and income documents in seconds.
        </p>
      </div>

      <StatsCards
        approvedCount={
          allApplicants.filter(
            (a) => !mockApplicants.includes(a) && a.status === "Approved",
          ).length
        }
        reviewCount={
          allApplicants.filter(
            (a) => !mockApplicants.includes(a) && a.status === "Review Needed",
          ).length
        }
      />

      <section className="space-y-2">
        <h2 className="text-lg font-semibold tracking-tight text-zinc-900">
          Verify a new applicant
        </h2>

        {view.status === "idle" && (
          <>
            <UploadArea
              onUpload={handleFileUpload}
              docsUsed={docsUsed}
              sessionLimit={SESSION_LIMIT}
            />
            <SampleDocumentCards onSampleClick={handleSampleClick} />
          </>
        )}

        {view.status === "processing" && (
          <ProcessingView
            file={view.file}
            sampleId={view.sampleId}
            onComplete={handleComplete}
            onError={handleError}
          />
        )}

        {view.status === "results" && (
          <ResultsView
            result={view.result}
            previewUrl={view.previewUrl}
            onApprove={handleApprove}
            onFlagForReview={handleFlagForReview}
            onReprocess={() =>
              setView({
                status: "processing",
                file: null,
                sampleId: null,
              })
            }
            onNewDocument={handleNewDocument}
          />
        )}

        {view.status === "error" && (
          <Card className="border-red-200 bg-red-50">
            <CardContent>
              <div className="flex items-start gap-3">
                <AlertTriangle className="mt-0.5 size-5 shrink-0 text-red-600" />
                <div className="flex-1">
                  <p className="font-medium text-red-800">
                    Document processing failed
                  </p>
                  <p className="mt-1 text-sm text-red-700">{view.message}</p>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleNewDocument}
                >
                  <RotateCcw className="mr-1.5 size-3.5" />
                  Try Again
                </Button>
              </div>
            </CardContent>
          </Card>
        )}
      </section>

      <ApplicantQueue applicants={allApplicants} />
    </main>
  )
}

function resultToApplicant(
  result: ProcessResponse,
  fields: ExtractedField[],
  status: "Approved" | "Review Needed",
): Applicant {
  const nameField = fields.find(
    (f) =>
      f.field_name === "full_name" ||
      f.field_name === "employee_name" ||
      f.field_name === "account_holder_name",
  )

  return {
    id: result.id,
    name: nameField?.value ?? "Unknown Applicant",
    documents: [DOC_TAG_MAP[result.document_type]],
    status,
    risk: RISK_MAP[result.risk_score],
    verifiedDate: new Date().toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    }),
  }
}

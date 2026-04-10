import { useState } from "react"
import { AlertTriangle, Clock, FileText } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import type { ExtractedField, ProcessResponse } from "@/lib/types"

type Props = {
  result: ProcessResponse
  previewUrl: string | null
  onApprove: (editedFields: ExtractedField[]) => void
  onFlagForReview: () => void
  onReprocess: () => void
  onNewDocument: () => void
}

const TYPE_LABELS: Record<string, string> = {
  government_id: "Government ID",
  proof_of_address: "Proof of Address",
  income_verification: "Income Verification",
}

export function ResultsView({
  result,
  previewUrl,
  onApprove,
  onFlagForReview,
  onReprocess,
  onNewDocument,
}: Props) {
  const [fields, setFields] = useState<ExtractedField[]>(result.fields)

  const updateField = (index: number, value: string) => {
    setFields((prev) =>
      prev.map((f, i) => (i === index ? { ...f, value } : f)),
    )
  }

  const typeLabel = TYPE_LABELS[result.document_type] ?? result.document_type
  const subtypeLabel =
    result.document_subtype.charAt(0).toUpperCase() +
    result.document_subtype.slice(1).replace(/_/g, " ")

  return (
    <Card>
      <CardContent>
        <div className="flex flex-col gap-6 lg:flex-row">
          {/* Left panel: preview */}
          <div className="flex flex-col items-center gap-4 lg:w-2/5">
            <div className="flex size-full min-h-48 items-center justify-center rounded-lg bg-zinc-100">
              {previewUrl ? (
                <img
                  src={previewUrl}
                  alt="Document preview"
                  className="max-h-72 rounded-lg object-contain"
                />
              ) : (
                <FileText className="size-16 text-zinc-400" />
              )}
            </div>
            <Badge variant="secondary" className="text-sm">
              {typeLabel} — {subtypeLabel}
            </Badge>
            <div className="flex items-center gap-1 text-xs text-zinc-500">
              <Clock className="size-3" />
              Processed in {(result.processing_time_ms / 1000).toFixed(1)}s
            </div>
          </div>

          {/* Right panel: fields */}
          <div className="flex-1 space-y-4">
            {/* Risk score + document type confidence */}
            <div className="flex items-center gap-3">
              <RiskBadge score={result.risk_score} />
              <span className="text-xs text-zinc-500">
                {Math.round(result.document_type_confidence * 100)}% classification
                confidence
              </span>
            </div>

            {/* Expired warning */}
            {result.is_expired && (
              <div className="flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                <AlertTriangle className="size-4 shrink-0" />
                This document has expired. Additional verification may be
                required.
              </div>
            )}

            {/* Validation warnings */}
            {result.validation_warnings.length > 0 && (
              <div className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-700">
                <p className="font-medium">Validation warnings:</p>
                <ul className="mt-1 list-inside list-disc">
                  {result.validation_warnings.map((w) => (
                    <li key={w}>{w}</li>
                  ))}
                </ul>
              </div>
            )}

            <Separator />

            {/* Extracted fields */}
            <div className="space-y-3">
              {fields.map((field, i) => (
                <FieldRow
                  key={field.field_name}
                  field={field}
                  onChange={(v) => updateField(i, v)}
                />
              ))}
            </div>

            <Separator />

            {/* Actions */}
            <div className="flex flex-wrap items-center gap-3">
              <Button onClick={() => onApprove(fields)}>Approve</Button>
              <Button variant="outline" onClick={onFlagForReview}>
                Flag for Review
              </Button>
              <Button variant="ghost" onClick={onReprocess}>
                Re-process
              </Button>
              <div className="flex-1" />
              <Button variant="ghost" onClick={onNewDocument}>
                New Document
              </Button>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

function FieldRow({
  field,
  onChange,
}: {
  field: ExtractedField
  onChange: (value: string) => void
}) {
  const confPct = Math.round(field.confidence * 100)

  return (
    <div
      className={
        "flex items-center gap-3 rounded-lg px-3 py-2 " +
        (field.requires_review
          ? "border-l-4 border-l-amber-400 bg-amber-50/50"
          : "")
      }
    >
      <label className="w-36 shrink-0 text-sm font-medium text-zinc-700">
        {field.label}
      </label>
      <Input
        value={field.value ?? ""}
        onChange={(e) => onChange(e.target.value)}
        className="flex-1"
      />
      <ConfidenceBadge confidence={field.confidence} pct={confPct} />
    </div>
  )
}

function ConfidenceBadge({
  confidence,
  pct,
}: {
  confidence: number
  pct: number
}) {
  let cls: string
  if (confidence >= 0.9) {
    cls = "bg-emerald-100 text-emerald-700 border-transparent"
  } else if (confidence >= 0.7) {
    cls = "bg-amber-100 text-amber-700 border-transparent"
  } else {
    cls = "bg-red-100 text-red-700 border-transparent"
  }

  return (
    <Badge className={cls + " shrink-0 tabular-nums"}>
      {pct}%
    </Badge>
  )
}

function RiskBadge({ score }: { score: string }) {
  const config: Record<string, { label: string; cls: string }> = {
    low: {
      label: "Low Risk",
      cls: "bg-emerald-100 text-emerald-700 border-transparent",
    },
    medium: {
      label: "Medium Risk",
      cls: "bg-amber-100 text-amber-700 border-transparent",
    },
    high: {
      label: "High Risk",
      cls: "bg-red-100 text-red-700 border-transparent",
    },
  }
  const c = config[score] ?? config.low

  return <Badge className={c.cls + " text-sm"}>{c.label}</Badge>
}

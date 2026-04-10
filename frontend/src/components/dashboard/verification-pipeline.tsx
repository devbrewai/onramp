import {
  Check,
  FileText,
  Loader2,
  Search,
  ShieldCheck,
  Upload,
  X,
} from "lucide-react"
import type { ComponentType } from "react"
import { Card, CardContent } from "@/components/ui/card"
import type { PipelineStage, StageState } from "@/hooks/use-pipeline-animation"

const stageIcons: Record<
  PipelineStage,
  ComponentType<{ className?: string }>
> = {
  upload: Upload,
  classify: Search,
  extract: FileText,
  validate: ShieldCheck,
}

export function VerificationPipeline({ stages }: { stages: StageState[] }) {
  return (
    <Card>
      <CardContent>
        <h3 className="mb-6 text-base font-semibold text-zinc-900">
          Verifying Document
        </h3>
        <div className="flex items-start justify-between gap-2">
          {stages.map((stage, i) => (
            <div key={stage.stage} className="flex flex-1 items-start">
              <StageNode stage={stage} />
              {i < stages.length - 1 && <StageConnector done={stage.status === "complete"} />}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

function StageNode({ stage }: { stage: StageState }) {
  const Icon = stageIcons[stage.stage]
  return (
    <div className="flex flex-col items-center gap-2 text-center">
      <div
        className={
          "flex size-12 items-center justify-center rounded-full transition-all duration-300 " +
          statusCircleClass(stage.status)
        }
      >
        <StatusIcon status={stage.status} Icon={Icon} />
      </div>
      <span
        className={
          "text-xs font-medium " +
          (stage.status === "pending" ? "text-zinc-400" : "text-zinc-700")
        }
      >
        {stage.label}
      </span>
      {stage.elapsedMs !== null && (
        <span className="text-[10px] text-zinc-500">
          {(stage.elapsedMs / 1000).toFixed(1)}s
        </span>
      )}
    </div>
  )
}

function StageConnector({ done }: { done: boolean }) {
  return (
    <div
      className={
        "mt-6 h-0.5 flex-1 transition-colors duration-500 " +
        (done ? "bg-emerald-400" : "bg-zinc-200")
      }
    />
  )
}

function StatusIcon({
  status,
  Icon,
}: {
  status: StageState["status"]
  Icon: ComponentType<{ className?: string }>
}) {
  switch (status) {
    case "pending":
      return <Icon className="size-5 text-zinc-400" />
    case "active":
      return <Loader2 className="size-5 animate-spin text-emerald-600" />
    case "complete":
      return <Check className="size-5 text-white" />
    case "error":
      return <X className="size-5 text-white" />
  }
}

function statusCircleClass(status: StageState["status"]): string {
  switch (status) {
    case "pending":
      return "bg-zinc-100"
    case "active":
      return "bg-emerald-100"
    case "complete":
      return "bg-emerald-500"
    case "error":
      return "bg-red-500"
  }
}

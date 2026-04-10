import { useEffect, useRef, useState } from "react"
import type { ProcessResponse } from "@/lib/types"

export type PipelineStage = "upload" | "classify" | "extract" | "validate"
export type StageStatus = "pending" | "active" | "complete" | "error"

export type StageState = {
  stage: PipelineStage
  label: string
  status: StageStatus
  elapsedMs: number | null
}

const STAGE_DEFINITIONS: { stage: PipelineStage; label: string }[] = [
  { stage: "upload", label: "Reading document" },
  { stage: "classify", label: "Classifying type" },
  { stage: "extract", label: "Extracting fields" },
  { stage: "validate", label: "Validating data" },
]

// Stages 1-3 advance on fixed timers. Stage 4 waits for the API.
const STAGE_DELAYS_MS = [800, 1000, 1700]

function initialStages(): StageState[] {
  return STAGE_DEFINITIONS.map((def, i) => ({
    ...def,
    status: i === 0 ? "active" : "pending",
    elapsedMs: null,
  }))
}

export function usePipelineAnimation(apiPromise: Promise<ProcessResponse> | null): {
  stages: StageState[]
  isDone: boolean
  result: ProcessResponse | null
  error: string | null
} {
  const [stages, setStages] = useState<StageState[]>(initialStages)
  const [result, setResult] = useState<ProcessResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [apiResolved, setApiResolved] = useState(false)
  const timersRef = useRef<ReturnType<typeof setTimeout>[]>([])
  const startTimeRef = useRef(0)
  const stageStartRef = useRef(0)

  useEffect(() => {
    if (!apiPromise) return

    const now = performance.now()
    startTimeRef.current = now
    stageStartRef.current = now

    // Advance stages 0→1, 1→2, 2→3 on fixed timers
    let cumulativeDelay = 0
    for (let i = 0; i < STAGE_DELAYS_MS.length; i++) {
      cumulativeDelay += STAGE_DELAYS_MS[i]
      const stageIndex = i
      const timer = setTimeout(() => {
        const now = performance.now()
        setStages((prev) => {
          const next = [...prev]
          // Complete current stage
          next[stageIndex] = {
            ...next[stageIndex],
            status: "complete",
            elapsedMs: Math.round(now - stageStartRef.current),
          }
          // Activate next stage
          if (stageIndex + 1 < next.length) {
            next[stageIndex + 1] = {
              ...next[stageIndex + 1],
              status: "active",
            }
          }
          stageStartRef.current = now
          return next
        })
      }, cumulativeDelay)
      timersRef.current.push(timer)
    }

    // Track the API promise
    apiPromise
      .then((res) => {
        setResult(res)
        setApiResolved(true)
      })
      .catch((err: unknown) => {
        const message =
          err instanceof Error ? err.message : "An unexpected error occurred"
        setError(message)
        setApiResolved(true)
      })

    return () => {
      for (const t of timersRef.current) clearTimeout(t)
      timersRef.current = []
    }
  }, [apiPromise])

  // When both stage 3 timer is done AND API has resolved, complete stage 4
  useEffect(() => {
    if (!apiResolved) return

    setStages((prev) => {
      // Wait until stage 2 (extract, index 2) is complete
      if (prev[2].status !== "complete") return prev

      const next = [...prev]
      const now = performance.now()

      if (error) {
        next[3] = { ...next[3], status: "error", elapsedMs: null }
      } else {
        next[3] = {
          ...next[3],
          status: "complete",
          elapsedMs: Math.round(now - stageStartRef.current),
        }
      }
      return next
    })
  }, [apiResolved, error, stages])

  const isDone = stages[3].status === "complete" || stages[3].status === "error"

  return { stages, isDone, result, error }
}

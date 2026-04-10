import { useEffect, useState } from "react"
import { processFile, processSample } from "@/lib/api"
import type { ProcessResponse } from "@/lib/types"
import { usePipelineAnimation } from "@/hooks/use-pipeline-animation"
import { VerificationPipeline } from "@/components/dashboard/verification-pipeline"

type Props = {
  file: File | null
  sampleId: string | null
  onComplete: (result: ProcessResponse, previewUrl: string | null) => void
  onError: (message: string) => void
}

export function ProcessingView({
  file,
  sampleId,
  onComplete,
  onError,
}: Props) {
  // Create the API promise once on mount via lazy initializer
  const [apiPromise] = useState<Promise<ProcessResponse> | null>(() => {
    if (file) return processFile(file)
    if (sampleId) return processSample(sampleId)
    return null
  })

  const { stages, isDone, result, error } = usePipelineAnimation(apiPromise)

  useEffect(() => {
    if (!isDone) return

    if (error) {
      onError(error)
      return
    }

    if (result) {
      const previewUrl = file ? URL.createObjectURL(file) : null
      onComplete(result, previewUrl)
    }
  }, [isDone, result, error, file, onComplete, onError])

  return <VerificationPipeline stages={stages} />
}

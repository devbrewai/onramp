import type { ProcessResponse, SampleInfo } from "@/lib/types"

const BASE_URL = import.meta.env.VITE_API_URL ?? ""

export class ApiError extends Error {
  status: number

  constructor(status: number, message: string) {
    super(message)
    this.name = "ApiError"
    this.status = status
  }
}

async function request<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${url}`, init)
  if (!response.ok) {
    const body = await response
      .json()
      .catch(() => ({ detail: response.statusText }))
    throw new ApiError(
      response.status,
      (body as { detail?: string }).detail ?? "Request failed",
    )
  }
  return response.json() as Promise<T>
}

export async function processFile(file: File): Promise<ProcessResponse> {
  const form = new FormData()
  form.append("file", file)
  return request<ProcessResponse>("/api/process", {
    method: "POST",
    body: form,
  })
}

export async function processSample(
  sampleId: string,
): Promise<ProcessResponse> {
  const form = new FormData()
  form.append("sample_id", sampleId)
  return request<ProcessResponse>("/api/process", {
    method: "POST",
    body: form,
  })
}

export async function fetchSamples(): Promise<SampleInfo[]> {
  return request<SampleInfo[]>("/api/samples")
}

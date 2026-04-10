import { useRef, useState, type ChangeEvent, type DragEvent } from "react"
import { Upload } from "lucide-react"

const ACCEPTED_TYPES = new Set([
  "application/pdf",
  "image/png",
  "image/jpeg",
  "image/jpg",
])
const MAX_SIZE_MB = 10

type Props = {
  onUpload: (file: File) => void
  docsUsed?: number
  sessionLimit?: number
}

export function UploadArea({ onUpload, docsUsed, sessionLimit }: Props) {
  const [isDragOver, setIsDragOver] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  const limitReached =
    docsUsed !== undefined &&
    sessionLimit !== undefined &&
    docsUsed >= sessionLimit

  const validateAndUpload = (file: File) => {
    setError(null)
    if (!ACCEPTED_TYPES.has(file.type)) {
      setError("Unsupported file type. Please upload a PDF, PNG, or JPG.")
      return
    }
    if (file.size > MAX_SIZE_MB * 1024 * 1024) {
      setError(`File exceeds ${MAX_SIZE_MB}MB limit.`)
      return
    }
    onUpload(file)
  }

  const handleDragOver = (event: DragEvent<HTMLButtonElement>) => {
    event.preventDefault()
    setIsDragOver(true)
  }

  const handleDragLeave = (event: DragEvent<HTMLButtonElement>) => {
    event.preventDefault()
    setIsDragOver(false)
  }

  const handleDrop = (event: DragEvent<HTMLButtonElement>) => {
    event.preventDefault()
    setIsDragOver(false)
    const file = event.dataTransfer.files[0]
    if (file) validateAndUpload(file)
  }

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) validateAndUpload(file)
    // Reset input so the same file can be re-selected
    event.target.value = ""
  }

  const handleClick = () => {
    inputRef.current?.click()
  }

  return (
    <section aria-label="Document upload">
      <button
        type="button"
        onClick={limitReached ? undefined : handleClick}
        onDragOver={limitReached ? undefined : handleDragOver}
        onDragLeave={limitReached ? undefined : handleDragLeave}
        onDrop={limitReached ? undefined : handleDrop}
        disabled={limitReached}
        className={
          "flex w-full flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed px-6 py-16 text-center transition-colors " +
          (limitReached
            ? "cursor-not-allowed border-zinc-200 bg-zinc-50 opacity-60"
            : isDragOver
              ? "border-emerald-500 bg-emerald-50/60"
              : "border-zinc-300 bg-white hover:border-zinc-400 hover:bg-zinc-50")
        }
      >
        <span
          className={
            "flex size-12 items-center justify-center rounded-full transition-colors " +
            (limitReached
              ? "bg-zinc-100 text-zinc-400"
              : isDragOver
                ? "bg-emerald-100 text-emerald-700"
                : "bg-zinc-100 text-zinc-500")
          }
        >
          <Upload className="size-6" />
        </span>
        <div>
          <p className="text-base font-medium text-zinc-900">
            {limitReached
              ? "Session limit reached"
              : "Drop documents here or click to browse"}
          </p>
          <p className="mt-1 text-sm text-zinc-500">
            {limitReached
              ? "Refresh the page to start a new session"
              : "Supports PDF, PNG, JPG"}
          </p>
        </div>
      </button>
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.png,.jpg,.jpeg"
        onChange={handleChange}
        hidden
      />
      {error && (
        <p className="mt-2 text-center text-sm text-red-600">{error}</p>
      )}
      <p className="mt-3 text-center text-xs text-zinc-500">
        DEMO ONLY. Do not upload real identity documents.
      </p>
      {docsUsed !== undefined && sessionLimit !== undefined && (
        <p className="mt-1 text-center text-xs text-zinc-400">
          {docsUsed} of {sessionLimit} documents used this session
        </p>
      )}
    </section>
  )
}

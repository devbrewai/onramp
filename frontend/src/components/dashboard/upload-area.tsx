import { useRef, useState, type DragEvent } from "react"
import { Upload } from "lucide-react"

export function UploadArea() {
  const [isDragOver, setIsDragOver] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

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
    // File handling is wired up in DEV-110 (Frontend Integration milestone).
  }

  const handleClick = () => {
    inputRef.current?.click()
  }

  return (
    <section aria-label="Document upload">
      <button
        type="button"
        onClick={handleClick}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={
          "flex w-full flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed px-6 py-16 text-center transition-colors " +
          (isDragOver
            ? "border-emerald-500 bg-emerald-50/60"
            : "border-zinc-300 bg-white hover:border-zinc-400 hover:bg-zinc-50")
        }
      >
        <span
          className={
            "flex size-12 items-center justify-center rounded-full transition-colors " +
            (isDragOver
              ? "bg-emerald-100 text-emerald-700"
              : "bg-zinc-100 text-zinc-500")
          }
        >
          <Upload className="size-6" />
        </span>
        <div>
          <p className="text-base font-medium text-zinc-900">
            Drop documents here or click to browse
          </p>
          <p className="mt-1 text-sm text-zinc-500">Supports PDF, PNG, JPG</p>
        </div>
      </button>
      <input ref={inputRef} type="file" accept=".pdf,.png,.jpg,.jpeg" hidden />
      <p className="mt-3 text-center text-xs text-zinc-500">
        DEMO ONLY. Do not upload real identity documents.
      </p>
    </section>
  )
}

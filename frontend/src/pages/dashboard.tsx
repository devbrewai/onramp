import { ApplicantQueue } from "@/components/dashboard/applicant-queue"
import { SampleDocumentCards } from "@/components/dashboard/sample-document-cards"
import { StatsCards } from "@/components/dashboard/stats-cards"
import { UploadArea } from "@/components/dashboard/upload-area"

export function Dashboard() {
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
      <StatsCards />
      <section className="space-y-2">
        <h2 className="text-lg font-semibold tracking-tight text-zinc-900">
          Verify a new applicant
        </h2>
        <UploadArea />
        <SampleDocumentCards />
      </section>
      <ApplicantQueue />
    </main>
  )
}

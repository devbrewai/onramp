import { type ComponentType } from "react"
import { IdCard, MapPin, Receipt } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  sampleDocuments,
  type SampleDocument,
  type SampleDocumentType,
} from "@/lib/mock-data"

const iconForType: Record<
  SampleDocumentType,
  ComponentType<{ className?: string }>
> = {
  government_id: IdCard,
  proof_of_address: MapPin,
  income_verification: Receipt,
}

export function SampleDocumentCards() {
  return (
    <section aria-label="Sample documents" className="mt-6">
      <h3 className="mb-3 text-sm font-medium text-zinc-700">
        Or try a sample:
      </h3>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {sampleDocuments.map((doc) => (
          <SampleCard key={doc.id} doc={doc} />
        ))}
      </div>
    </section>
  )
}

function SampleCard({ doc }: { doc: SampleDocument }) {
  const Icon = iconForType[doc.type]
  return (
    <Card className="group cursor-pointer transition-colors hover:border-emerald-400 hover:shadow-sm">
      <CardContent>
        <div className="flex items-start gap-3">
          <span className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700 transition-colors group-hover:bg-emerald-100">
            <Icon className="size-5" />
          </span>
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-semibold text-zinc-900">
              {doc.name}
            </p>
            <Badge
              variant="secondary"
              className="mt-1 bg-zinc-100 text-zinc-600"
            >
              {doc.typeLabel}
            </Badge>
            <p className="mt-2 text-xs text-zinc-500">{doc.description}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

import { Badge } from "@/components/ui/badge"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import type { Applicant, ApplicantStatus, RiskLevel } from "@/lib/mock-data"

const statusBadgeClass: Record<ApplicantStatus, string> = {
  Approved: "bg-emerald-100 text-emerald-700 border-transparent",
  "Review Needed": "bg-amber-100 text-amber-700 border-transparent",
  Flagged: "bg-red-100 text-red-700 border-transparent",
}

const riskBadgeClass: Record<RiskLevel, string> = {
  Low: "bg-zinc-100 text-zinc-700 border-transparent",
  Medium: "bg-amber-100 text-amber-700 border-transparent",
  High: "bg-red-100 text-red-700 border-transparent",
}

export function ApplicantQueue({ applicants }: { applicants: Applicant[] }) {
  return (
    <section aria-label="Applicant queue">
      <div className="mb-3 flex items-baseline justify-between">
        <h2 className="text-lg font-semibold tracking-tight text-zinc-900">
          Applicant Queue
        </h2>
        <p className="text-xs text-zinc-500">
          {applicants.length} verified applicants
        </p>
      </div>
      <div className="overflow-x-auto rounded-xl border border-zinc-200 bg-white">
        <Table>
          <TableHeader>
            <TableRow className="bg-zinc-50/60">
              <TableHead className="text-zinc-600">Applicant</TableHead>
              <TableHead className="text-zinc-600">Documents</TableHead>
              <TableHead className="text-zinc-600">Status</TableHead>
              <TableHead className="text-zinc-600">Risk Score</TableHead>
              <TableHead className="text-zinc-600">Verified Date</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {applicants.map((applicant) => (
              <TableRow key={applicant.id}>
                <TableCell className="font-medium text-zinc-900">
                  {applicant.name}
                </TableCell>
                <TableCell className="text-zinc-600">
                  {applicant.documents.join(", ")}
                </TableCell>
                <TableCell>
                  <Badge className={statusBadgeClass[applicant.status]}>
                    {applicant.status}
                  </Badge>
                </TableCell>
                <TableCell>
                  <Badge className={riskBadgeClass[applicant.risk]}>
                    {applicant.risk}
                  </Badge>
                </TableCell>
                <TableCell className="text-zinc-600">
                  {applicant.verifiedDate}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </section>
  )
}

import { Card, CardContent } from "@/components/ui/card"
import { dashboardStats } from "@/lib/mock-data"

const numberFormatter = new Intl.NumberFormat("en-US")
const percentFormatter = new Intl.NumberFormat("en-US", {
  style: "percent",
  maximumFractionDigits: 0,
})

type Props = {
  approvedCount: number
  reviewCount: number
}

type Stat = {
  label: string
  value: string
  helper: string
}

function buildStats(approvedCount: number, reviewCount: number): Stat[] {
  return [
    {
      label: "Applicants Processed",
      value: numberFormatter.format(
        dashboardStats.applicantsProcessed + approvedCount + reviewCount,
      ),
      helper: "Last 30 days",
    },
    {
      label: "Avg Verification Time",
      value: `${dashboardStats.avgVerificationSeconds}s`,
      helper: "vs. 24-48hr manual review",
    },
    {
      label: "Auto-Approval Rate",
      value: percentFormatter.format(dashboardStats.autoApprovalRate),
      helper: "Approved without human review",
    },
    {
      label: "Pending Review",
      value: numberFormatter.format(
        dashboardStats.pendingReview + reviewCount,
      ),
      helper: "Awaiting compliance team",
    },
  ]
}

export function StatsCards({ approvedCount, reviewCount }: Props) {
  const stats = buildStats(approvedCount, reviewCount)
  return (
    <section
      aria-label="Dashboard statistics"
      className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4"
    >
      {stats.map((stat) => (
        <Card key={stat.label}>
          <CardContent>
            <p className="text-sm font-medium text-zinc-500">{stat.label}</p>
            <p className="mt-2 text-3xl font-semibold tracking-tight text-zinc-900">
              {stat.value}
            </p>
            <p className="mt-1 text-xs text-zinc-500">{stat.helper}</p>
          </CardContent>
        </Card>
      ))}
    </section>
  )
}

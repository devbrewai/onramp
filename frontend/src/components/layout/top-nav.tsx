import { Menu } from "lucide-react"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"

const navLinks = [
  { label: "Dashboard", active: true },
  { label: "Applicants", active: false },
  { label: "Documents", active: false },
  { label: "Settings", active: false },
] as const

export function TopNav() {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-zinc-200 bg-white">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-8">
          <span className="text-xl font-semibold tracking-tight text-zinc-900">
            <span className="text-emerald-600">O</span>nramp
          </span>
          <nav className="hidden md:flex md:items-center md:gap-1">
            {navLinks.map((link) => (
              <a
                key={link.label}
                href="#"
                aria-current={link.active ? "page" : undefined}
                className={
                  link.active
                    ? "rounded-md px-3 py-2 text-sm font-medium text-emerald-700"
                    : "rounded-md px-3 py-2 text-sm font-medium text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900"
                }
              >
                {link.label}
              </a>
            ))}
          </nav>
        </div>
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            aria-label="Open navigation menu"
          >
            <Menu className="size-5" />
          </Button>
          <Avatar className="size-9">
            <AvatarFallback className="bg-emerald-100 text-sm font-medium text-emerald-700">
              AR
            </AvatarFallback>
          </Avatar>
        </div>
      </div>
    </header>
  )
}

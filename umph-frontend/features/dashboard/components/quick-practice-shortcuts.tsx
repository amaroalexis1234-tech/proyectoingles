import Link from "next/link";
import { BookOpen, ClipboardCheck, PenSquare, SpellCheck } from "lucide-react";

import { Card } from "@/components/ui/card";

const SHORTCUTS = [
  { href: "/practice/reading", label: "Reading", description: "Improve comprehension", icon: BookOpen, color: "text-primary bg-primary/10" },
  { href: "/practice/structure", label: "Structure", description: "Master grammar rules", icon: PenSquare, color: "text-accent-green bg-accent-green/10" },
  { href: "/practice/written-expression", label: "Written Expression", description: "Build written accuracy", icon: SpellCheck, color: "text-accent-purple bg-accent-purple/10" },
  { href: "/evaluations/mini-test", label: "Mini Test", description: "Practice short tests", icon: ClipboardCheck, color: "text-accent-orange bg-accent-orange/10" },
];

/**
 * Grilla estatica de atajos, sin llamada a backend -- distinta del
 * RecommendedPracticeCard dinamico (secciones debiles).
 */
export function QuickPracticeShortcuts() {
  return (
    <div>
      <div className="mb-3 flex items-center justify-between">
        <div>
          <h2 className="text-base font-semibold text-foreground">Quick Practice</h2>
          <p className="text-sm text-foreground-muted">Jump into a section</p>
        </div>
        <Link href="/practice" className="text-sm font-medium text-primary hover:underline">
          Ver todas →
        </Link>
      </div>

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        {SHORTCUTS.map(({ href, label, description, icon: Icon, color }) => (
          <Link key={href} href={href}>
            <Card className="flex h-full items-center gap-3 p-4 transition-colors hover:border-primary">
              <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded ${color}`}>
                <Icon className="h-5 w-5" />
              </div>
              <div className="min-w-0">
                <p className="truncate text-sm font-medium text-foreground">{label}</p>
                <p className="truncate text-xs text-foreground-muted">{description}</p>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}

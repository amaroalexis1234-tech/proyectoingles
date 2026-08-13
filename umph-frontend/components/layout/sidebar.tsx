"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BarChart3,
  BookOpen,
  ClipboardCheck,
  History,
  LayoutDashboard,
  Monitor,
  PenSquare,
  Settings,
  SpellCheck,
  User,
} from "lucide-react";

import { LevelBadge } from "@/components/layout/level-badge";
import { useDashboardSummary } from "@/features/progress/hooks/use-dashboard-summary";
import { cn } from "@/lib/utils";

export const NAV_ITEMS = [
  { href: "/dashboard", label: "Inicio", icon: LayoutDashboard },
  { href: "/practice/reading", label: "Reading", icon: BookOpen },
  { href: "/practice/structure", label: "Structure", icon: PenSquare },
  { href: "/practice/written-expression", label: "Written Expression", icon: PenSquare },
  { href: "/practice/vocabulary", label: "Vocabulary", icon: SpellCheck },
  { href: "/evaluations/mini-test", label: "Mini Tests", icon: ClipboardCheck },
  { href: "/evaluations/simulator", label: "Official Simulator", icon: Monitor },
  { href: "/stats", label: "Estadísticas", icon: BarChart3 },
  { href: "/history", label: "Historial", icon: History },
  { href: "/profile", label: "Perfil", icon: User },
  { href: "/settings", label: "Configuración", icon: Settings },
];

/**
 * Componente global unico: se usa igual en todos los modulos (app)/*.
 * Nunca se crea una variante distinta por pantalla -- si un modulo
 * necesita algo especial, va dentro del contenido, no aqui.
 */
export function Sidebar() {
  const pathname = usePathname();
  const { data: summary } = useDashboardSummary();

  return (
    <aside className="hidden w-64 shrink-0 flex-col border-r border-border bg-surface md:flex">
      <div className="flex h-16 items-center px-6">
        <span className="text-lg font-semibold tracking-tight text-foreground">
          UPMH <span className="text-primary">English Prep</span>
        </span>
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-4">
        {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
          const isActive = pathname === href || pathname.startsWith(`${href}/`);
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-3 rounded px-3 py-2.5 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary/10 text-primary"
                  : "text-foreground-muted hover:bg-background hover:text-foreground"
              )}
            >
              <Icon className="h-4 w-4" />
              {label}
            </Link>
          );
        })}
      </nav>

      {summary && (
        <div className="p-3">
          <LevelBadge xpLevel={summary.xp_level} level={summary.level} variant="card" />
        </div>
      )}
    </aside>
  );
}

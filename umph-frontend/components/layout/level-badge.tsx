import { Progress } from "@/components/ui/progress";
import type { LevelEstimate, XpLevel } from "@/features/progress/api";
import { cn } from "@/lib/utils";

interface LevelBadgeProps {
  xpLevel: XpLevel;
  level: LevelEstimate | null;
  variant?: "card" | "compact";
}

/**
 * Un solo componente compartido por Sidebar (card completa) y Header
 * (compacto) -- nunca se forkea, se le pasa la data ya cargada por quien
 * lo use. cefr_band viene de evaluaciones reales; el progreso mostrado es
 * el de XP (level.cefr_band solo aporta la etiqueta/color del badge).
 */
export function LevelBadge({ xpLevel, level, variant = "card" }: LevelBadgeProps) {
  const bandLabel = level?.cefr_band ?? "—";
  const progressPercent = (xpLevel.current_xp_in_level / xpLevel.xp_for_next_level) * 100;

  if (variant === "compact") {
    return (
      <div
        className="hidden items-center gap-2 rounded border border-border bg-background px-3 py-1.5 sm:flex"
        title={level ? `Score estimado: ${level.estimated_score}/677` : "Aún no hay suficientes evaluaciones"}
      >
        <span className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-xs font-semibold text-primary-foreground">
          {bandLabel[0] ?? "?"}
        </span>
        <span className="text-xs font-medium text-foreground-muted">
          Nivel {xpLevel.level} · {bandLabel}
        </span>
      </div>
    );
  }

  return (
    <div className="rounded border border-border bg-background p-4">
      <div className="flex items-center gap-3">
        <span className="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-sm font-semibold text-primary-foreground">
          {bandLabel[0] ?? "?"}
        </span>
        <div>
          <p className="text-xs text-foreground-muted">Nivel estimado</p>
          <p className={cn("text-sm font-semibold text-foreground", !level && "text-foreground-muted")}>
            {level ? bandLabel : "Aún sin evaluar"}
          </p>
        </div>
      </div>

      <Progress value={progressPercent} className="mt-3" />
      <p className="mt-1.5 text-xs text-foreground-muted">
        {xpLevel.current_xp_in_level.toLocaleString()} / {xpLevel.xp_for_next_level.toLocaleString()} XP
      </p>
    </div>
  );
}

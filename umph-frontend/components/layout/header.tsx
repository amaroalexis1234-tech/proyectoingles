"use client";

import { motion } from "framer-motion";
import { Flame, Sparkles } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { LevelBadge } from "@/components/layout/level-badge";
import { UserMenu } from "@/components/layout/user-menu";
import { useDashboardSummary } from "@/features/progress/hooks/use-dashboard-summary";
import { usePrevious } from "@/lib/use-previous";

/**
 * Componente global unico, igual que Sidebar: nunca se modifica su
 * estructura entre modulos (segun el design system aprobado).
 */
export function Header() {
  const { data: summary } = useDashboardSummary();

  const previousXp = usePrevious(summary?.current_xp);
  const xpJustIncreased = previousXp !== undefined && summary != null && summary.current_xp > previousXp;

  const previousStreak = usePrevious(summary?.streak_days);
  const streakJustIncreased = previousStreak !== undefined && summary != null && summary.streak_days > previousStreak;

  return (
    <header className="flex h-16 items-center justify-end gap-3 border-b border-border bg-surface px-6">
      <Badge>
        <motion.span animate={xpJustIncreased ? { scale: [1, 1.5, 1], rotate: [0, -10, 10, 0] } : {}} transition={{ duration: 0.5 }}>
          <Sparkles className="h-3.5 w-3.5" />
        </motion.span>
        <motion.span animate={xpJustIncreased ? { scale: [1, 1.3, 1] } : {}} transition={{ duration: 0.4 }}>
          {summary?.current_xp ?? 0} XP
        </motion.span>
      </Badge>

      {summary && summary.streak_days > 0 && (
        <Badge variant="warning">
          <motion.span animate={streakJustIncreased ? { scale: [1, 1.6, 1], rotate: [0, -15, 15, 0] } : {}} transition={{ duration: 0.6 }}>
            <Flame className="h-3.5 w-3.5" />
          </motion.span>
          {summary.streak_days} {summary.streak_days === 1 ? "día" : "días"}
        </Badge>
      )}

      {summary && <LevelBadge xpLevel={summary.xp_level} level={summary.level} variant="compact" />}

      <UserMenu />
    </header>
  );
}

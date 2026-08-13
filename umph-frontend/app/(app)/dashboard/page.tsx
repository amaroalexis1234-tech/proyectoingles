"use client";

import { BookOpen, Target } from "lucide-react";

import { ContinuePracticeCard } from "@/features/dashboard/components/continue-practice-card";
import { DailyGoalCard } from "@/features/dashboard/components/daily-goal-card";
import { EmptyStateCard } from "@/features/dashboard/components/empty-state-card";
import { QuickPracticeShortcuts } from "@/features/dashboard/components/quick-practice-shortcuts";
import { RecommendedPracticeCard } from "@/features/dashboard/components/recommended-practice-card";
import { StreakFreezeCard } from "@/features/dashboard/components/streak-freeze-card";
import { WeakSkillsCard } from "@/features/dashboard/components/weak-skills-card";
import { useInProgressAttempt } from "@/features/evaluations/hooks/use-in-progress-attempt";
import { ProgressChart } from "@/features/progress/components/progress-chart";
import { StudyStatisticsGrid } from "@/features/progress/components/study-statistics-grid";
import { useDashboardSummary } from "@/features/progress/hooks/use-dashboard-summary";
import { useStudyStatistics } from "@/features/progress/hooks/use-study-statistics";

export default function DashboardPage() {
  const { data: summary, isLoading } = useDashboardSummary();
  const { data: inProgressAttempt } = useInProgressAttempt();
  const { data: stats } = useStudyStatistics();

  if (isLoading || !summary) {
    return (
      <div className="p-6">
        <div className="h-6 w-40 animate-pulse rounded bg-surface" />
      </div>
    );
  }

  return (
    <div className="animate-fade-in space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Tu progreso</h1>
        <p className="text-sm text-foreground-muted">Resumen de tu actividad en UPMH English Prep.</p>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {inProgressAttempt && <ContinuePracticeCard attempt={inProgressAttempt} />}
        <DailyGoalCard goal={summary.daily_goal} />
        {summary.has_enough_data_for_recommendations ? (
          <WeakSkillsCard skills={summary.weak_skills} />
        ) : (
          <EmptyStateCard
            icon={Target}
            title="Weak Skills"
            description="Detectamos automáticamente en qué necesitas practicar más."
            hint="Completa algunos ejercicios de práctica para que empecemos a identificar tus áreas de oportunidad."
          />
        )}
        <StreakFreezeCard streakDays={summary.streak_days} freezeAvailable={summary.streak_freeze_available} />
      </div>

      <QuickPracticeShortcuts />

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <ProgressChart />
        {summary.has_enough_data_for_recommendations ? (
          <RecommendedPracticeCard suggestions={summary.quick_practice} />
        ) : (
          <EmptyStateCard
            icon={BookOpen}
            title="Recomendado para ti"
            description="Ejercicios sugeridos según tu actividad reciente."
            hint="Aún no tenemos suficiente actividad tuya para sugerirte algo personalizado — mientras tanto, explora la sección de Práctica."
          />
        )}
      </div>

      {stats && <StudyStatisticsGrid stats={stats} />}
    </div>
  );
}

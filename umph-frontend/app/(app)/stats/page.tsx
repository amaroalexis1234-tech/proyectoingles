"use client";

import type { LucideIcon } from "lucide-react";
import { CheckSquare, ClipboardCheck, Clock, Flame, Monitor, Sparkles } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AccuracyDonut } from "@/features/progress/components/accuracy-donut";
import { RecentExamsChart } from "@/features/progress/components/recent-exams-chart";
import { WeeklyEvolutionChart } from "@/features/progress/components/weekly-evolution-chart";
import { useDashboardSummary } from "@/features/progress/hooks/use-dashboard-summary";
import { useStudyStatistics } from "@/features/progress/hooks/use-study-statistics";

function formatStudyTime(totalSeconds: number): string {
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  if (hours === 0) return `${minutes}m`;
  return `${hours}h ${minutes}m`;
}

interface Tile {
  icon: LucideIcon;
  label: string;
  value: string;
  color: string;
}

export default function StatsPage() {
  const { data: stats, isLoading } = useStudyStatistics();
  const { data: summary } = useDashboardSummary();

  if (isLoading || !stats) {
    return (
      <div className="p-6">
        <div className="h-6 w-40 animate-pulse rounded bg-surface" />
      </div>
    );
  }

  const tiles: Tile[] = [
    { icon: Clock, label: "Tiempo estudiado", value: formatStudyTime(stats.study_time_seconds), color: "text-primary bg-primary/10" },
    { icon: CheckSquare, label: "Preguntas respondidas", value: stats.questions_answered.toLocaleString(), color: "text-accent-green bg-accent-green/10" },
    { icon: ClipboardCheck, label: "Mini Tests realizados", value: String(stats.completed_mini_tests), color: "text-accent-purple bg-accent-purple/10" },
    { icon: Monitor, label: "Simuladores completados", value: String(stats.completed_simulators), color: "text-accent-orange bg-accent-orange/10" },
    { icon: Flame, label: "Racha actual", value: `${stats.day_streak} días`, color: "text-warning bg-warning/10" },
    { icon: Sparkles, label: "XP Total", value: (summary?.current_xp ?? 0).toLocaleString(), color: "text-primary bg-primary/10" },
  ];

  return (
    <div className="animate-fade-in space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Tu progreso</h1>
        <p className="text-sm text-foreground-muted">Visualiza tu rendimiento y evolución a lo largo del tiempo.</p>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Precisión general</CardTitle>
          </CardHeader>
          <CardContent>
            <AccuracyDonut
              correct={stats.correct_count}
              incorrect={stats.incorrect_count}
              unanswered={stats.unanswered_count}
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Resultados de los últimos exámenes</CardTitle>
          </CardHeader>
          <CardContent>
            <RecentExamsChart />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Evolución semanal</CardTitle>
        </CardHeader>
        <CardContent>
          <WeeklyEvolutionChart />
        </CardContent>
      </Card>

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-3">
        {tiles.map(({ icon: Icon, label, value, color }) => (
          <Card key={label} className="flex items-center gap-3 p-4">
            <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded ${color}`}>
              <Icon className="h-5 w-5" />
            </div>
            <div className="min-w-0">
              <p className="truncate text-lg font-semibold text-foreground">{value}</p>
              <p className="truncate text-xs text-foreground-muted">{label}</p>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

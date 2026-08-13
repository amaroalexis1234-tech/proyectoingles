import type { LucideIcon } from "lucide-react";
import { CheckSquare, Clock, Flame, ListChecks, Monitor, Target } from "lucide-react";

import { Card } from "@/components/ui/card";
import type { StudyStatistics } from "@/features/progress/api";

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

export function StudyStatisticsGrid({ stats }: { stats: StudyStatistics }) {
  const tiles: Tile[] = [
    { icon: ListChecks, label: "Questions Answered", value: stats.questions_answered.toLocaleString(), color: "text-primary bg-primary/10" },
    { icon: CheckSquare, label: "Accuracy", value: stats.accuracy_percent != null ? `${stats.accuracy_percent}%` : "—", color: "text-success bg-success/10" },
    { icon: Clock, label: "Study Time", value: formatStudyTime(stats.study_time_seconds), color: "text-accent-purple bg-accent-purple/10" },
    { icon: Monitor, label: "Completed Simulators", value: String(stats.completed_simulators), color: "text-accent-orange bg-accent-orange/10" },
    { icon: Target, label: "Completed Mini Tests", value: String(stats.completed_mini_tests), color: "text-accent-green bg-accent-green/10" },
    { icon: Flame, label: "Day Streak", value: String(stats.day_streak), color: "text-warning bg-warning/10" },
  ];

  return (
    <div>
      <h2 className="mb-1 text-base font-semibold text-foreground">Study Statistics</h2>
      <p className="mb-3 text-sm text-foreground-muted">Overview of your activity</p>

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

import { Flame, Sparkles } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import type { DashboardSummary } from "@/features/progress/api";

export function SummaryCards({ summary }: { summary: DashboardSummary }) {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
      <Card>
        <CardContent className="flex items-center gap-4 space-y-0">
          <div className="flex h-12 w-12 items-center justify-center rounded bg-primary/10 text-primary">
            <Sparkles className="h-6 w-6" />
          </div>
          <div>
            <p className="text-2xl font-semibold text-foreground">{summary.current_xp}</p>
            <p className="text-sm text-foreground-muted">XP total</p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="flex items-center gap-4 space-y-0">
          <div className="flex h-12 w-12 items-center justify-center rounded bg-warning/10 text-warning">
            <Flame className="h-6 w-6" />
          </div>
          <div>
            <p className="text-2xl font-semibold text-foreground">{summary.streak_days}</p>
            <p className="text-sm text-foreground-muted">
              {summary.streak_days === 1 ? "día de racha" : "días de racha"}
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

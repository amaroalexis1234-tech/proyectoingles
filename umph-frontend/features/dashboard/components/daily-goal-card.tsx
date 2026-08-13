import { Target } from "lucide-react";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import type { DailyGoal } from "@/features/progress/api";

export function DailyGoalCard({ goal }: { goal: DailyGoal }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <Target className="h-4 w-4 text-foreground-muted" />
          Today&apos;s Goal
        </CardTitle>
        <CardDescription>Responde {goal.target_count} preguntas hoy.</CardDescription>
      </CardHeader>
      <CardContent>
        <p className="mb-2 text-sm text-foreground">
          {goal.completed_count} / {goal.target_count} Completed
        </p>
        <Progress value={(goal.completed_count / goal.target_count) * 100} />
        {goal.completed && <p className="mt-2 text-sm text-success">¡Meta completada hoy!</p>}
      </CardContent>
    </Card>
  );
}

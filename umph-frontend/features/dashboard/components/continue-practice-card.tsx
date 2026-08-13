import Link from "next/link";
import { PlayCircle } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import type { InProgressAttempt } from "@/features/evaluations/api";

const MODE_LABELS: Record<string, string> = {
  grammar: "Grammar",
  reading: "Reading",
  mixed: "Mixed",
  official: "Official",
};

/**
 * Solo existe para evaluaciones (unico lugar con dato real de "en progreso"
 * hoy) -- se omite por completo, no se fabrica, si no hay ninguna.
 */
export function ContinuePracticeCard({ attempt }: { attempt: InProgressAttempt }) {
  const isSimulator = attempt.test_type === "simulator";
  const label = isSimulator ? "Official Simulator" : MODE_LABELS[attempt.mini_test_mode ?? ""] ?? "Mini Test";
  const href = isSimulator
    ? `/evaluations/simulator?attempt=${attempt.id}`
    : `/evaluations/mini-test?attempt=${attempt.id}`;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <PlayCircle className="h-4 w-4 text-foreground-muted" />
          Continue Practice
        </CardTitle>
        <CardDescription>Retoma donde lo dejaste.</CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-sm font-medium text-foreground">{label}</p>
        <p className="mb-2 text-sm text-foreground-muted">
          {attempt.answered_count} / {attempt.total_questions} preguntas
        </p>
        <Progress value={(attempt.answered_count / attempt.total_questions) * 100} className="mb-4" />
        <Button asChild size="sm" className="w-full">
          <Link href={href}>Continuar</Link>
        </Button>
      </CardContent>
    </Card>
  );
}

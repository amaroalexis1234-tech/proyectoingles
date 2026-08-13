"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useQuestionAnalytics } from "@/features/teacher/hooks/use-question-bank";
import { cn } from "@/lib/utils";

const SECTION_LABELS: Record<string, string> = {
  structure: "Structure",
  written_expression: "Written Expression",
  reading: "Reading",
  vocabulary: "Vocabulary",
};

function accuracyColor(percent: number): string {
  if (percent < 50) return "text-error";
  if (percent < 75) return "text-warning";
  return "text-success";
}

export default function TeacherAnalyticsPage() {
  const { data, isLoading } = useQuestionAnalytics();

  if (isLoading || !data) {
    return (
      <div className="p-6">
        <div className="h-6 w-40 animate-pulse rounded bg-surface" />
      </div>
    );
  }

  return (
    <div className="animate-fade-in space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Analítica de preguntas</h1>
        <p className="text-sm text-foreground-muted">
          Precisión real de cada pregunta (Mini Tests, Simulador y práctica libre), de menor a mayor acierto — las
          primeras son las que más vale la pena revisar.
        </p>
      </div>

      {data.untried_count > 0 && (
        <p className="text-sm text-foreground-muted">
          {data.untried_count} pregunta{data.untried_count === 1 ? "" : "s"} del banco todavía no{" "}
          {data.untried_count === 1 ? "ha" : "han"} sido respondida{data.untried_count === 1 ? "" : "s"} por ningún
          alumno, así que no aparece{data.untried_count === 1 ? "" : "n"} aquí.
        </p>
      )}

      {data.questions.length === 0 ? (
        <Card>
          <CardContent className="pt-2 text-sm text-foreground-muted">
            Todavía no hay preguntas respondidas para analizar.
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {data.questions.map((q) => (
            <Card key={q.question_id}>
              <CardContent className="space-y-2 pt-2">
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <Badge variant="secondary" className="mb-1">
                      {SECTION_LABELS[q.section] ?? q.section}
                    </Badge>
                    <p className="text-sm text-foreground">{q.prompt}</p>
                  </div>
                  <p className={cn("shrink-0 text-lg font-semibold", accuracyColor(q.accuracy_percent))}>
                    {q.accuracy_percent}%
                  </p>
                </div>
                <Progress value={q.accuracy_percent} />
                <p className="text-xs text-foreground-muted">
                  {q.correct_count} de {q.attempts_count} intento{q.attempts_count === 1 ? "" : "s"} correcto
                  {q.correct_count === 1 ? "" : "s"}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

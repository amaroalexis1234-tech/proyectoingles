"use client";

import { useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { Clock, Sparkles, Target, XCircle } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useRecommendPractice } from "@/features/ai/hooks/use-recommend-practice";
import { SimpleDonut } from "@/features/progress/components/simple-donut";
import { useDashboardSummary } from "@/features/progress/hooks/use-dashboard-summary";
import { useTestResult } from "@/features/progress/hooks/use-test-result";

const SECTION_LABELS: Record<string, string> = {
  structure: "Structure",
  written_expression: "Written Expression",
  reading: "Reading",
  vocabulary: "Vocabulary",
};

const SECTION_ROUTES: Record<string, string> = {
  structure: "/practice/structure",
  written_expression: "/practice/written-expression",
  reading: "/practice/reading",
  vocabulary: "/practice/vocabulary",
};

function qualityLabel(percent: number): { text: string; className: string } {
  if (percent >= 85) return { text: "Excelente", className: "text-success" };
  if (percent >= 80) return { text: "Bueno", className: "text-primary" };
  return { text: "Regular", className: "text-warning" };
}

export default function ResultsPage() {
  const { attemptId } = useParams<{ attemptId: string }>();
  const { data: result, isLoading } = useTestResult(attemptId);
  const { data: summary } = useDashboardSummary();
  const recommend = useRecommendPractice();

  useEffect(() => {
    if (attemptId) recommend.mutate(attemptId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [attemptId]);

  if (isLoading || !result) {
    return (
      <div className="p-6">
        <div className="h-6 w-40 animate-pulse rounded bg-surface" />
      </div>
    );
  }

  const durationMinutes = Math.max(
    1,
    Math.round((new Date(result.completed_at).getTime() - new Date(result.started_at).getTime()) / 60000)
  );
  const incorrectCount = result.total_questions - result.correct_count;

  const sectionEntries = Object.entries(result.section_scores).filter(([, score]) => score.total > 0);
  const weakestSection = sectionEntries.reduce<{ section: string; percent: number } | null>((worst, [section, score]) => {
    const percent = (score.correct / score.total) * 100;
    if (!worst || percent < worst.percent) return { section, percent };
    return worst;
  }, null);

  return (
    <div className="animate-fade-in mx-auto max-w-4xl space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Resultados</h1>
        <p className="text-sm text-foreground-muted">Revisa tu desempeño en este examen.</p>
      </div>

      <Card>
        <CardContent className="flex flex-col items-center gap-8 pt-2 sm:flex-row sm:items-center">
          <SimpleDonut percent={result.accuracy} label="Calificación" />

          <div className="grid flex-1 grid-cols-2 gap-4">
            <div className="flex items-center gap-2">
              <Clock className="h-4 w-4 text-foreground-muted" />
              <div>
                <p className="text-xs text-foreground-muted">Tiempo empleado</p>
                <p className="text-sm font-medium text-foreground">{durationMinutes} minutos</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Target className="h-4 w-4 text-foreground-muted" />
              <div>
                <p className="text-xs text-foreground-muted">Nivel estimado</p>
                <p className="text-sm font-medium text-foreground">
                  {summary?.level ? `${summary.level.cefr_band}` : "Aún sin evaluar"}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-success" />
              <div>
                <p className="text-xs text-foreground-muted">Preguntas correctas</p>
                <p className="text-sm font-medium text-foreground">{result.correct_count}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <XCircle className="h-4 w-4 text-error" />
              <div>
                <p className="text-xs text-foreground-muted">Preguntas incorrectas</p>
                <p className="text-sm font-medium text-foreground">{incorrectCount}</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        {sectionEntries.map(([section, score]) => {
          const percent = Math.round((score.correct / score.total) * 100);
          const quality = qualityLabel(percent);
          return (
            <Card key={section}>
              <p className="mb-1 font-semibold text-foreground">{SECTION_LABELS[section] ?? section}</p>
              <p className="mb-2 text-2xl font-semibold text-foreground">{percent}%</p>
              <Progress value={percent} className="mb-2" />
              <p className={`text-sm font-medium ${quality.className}`}>{quality.text}</p>
            </Card>
          );
        })}
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <Sparkles className="h-4 w-4 text-primary" />
            Recomendaciones de IA
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {recommend.isPending || !recommend.data ? (
            <div className="space-y-2">
              <div className="h-4 w-full animate-pulse rounded bg-surface" />
              <div className="h-4 w-2/3 animate-pulse rounded bg-surface" />
            </div>
          ) : (
            <>
              <p className="text-sm text-foreground">{recommend.data.recommendation}</p>
              {weakestSection && (
                <Button asChild size="sm">
                  <Link href={SECTION_ROUTES[weakestSection.section] ?? "/practice"}>
                    Practicar ahora
                    <span aria-hidden="true">→</span>
                  </Link>
                </Button>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

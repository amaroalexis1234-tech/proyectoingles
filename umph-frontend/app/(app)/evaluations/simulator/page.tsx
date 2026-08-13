"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { AlertTriangle, BookOpen, Clock, ClipboardList, Headphones, PenSquare, SpellCheck } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { fetchAttempt } from "@/features/evaluations/api";
import { TestRunner } from "@/features/evaluations/components/test-runner";
import { useStartSimulator } from "@/features/evaluations/hooks/use-start-simulator";
import type { TestAttemptStarted, TestResult } from "@/features/evaluations/api";

export default function SimulatorPage() {
  const router = useRouter();
  // Se lee directo de window.location en vez de useSearchParams(): en este
  // entorno, useSearchParams() envuelto en Suspense se queda colgado
  // indefinidamente cuando la URL no trae ningun query param -- este
  // componente es 100% cliente, no necesita el bailout de Suspense.
  const [resumeAttemptId, setResumeAttemptId] = useState<string | null>(null);
  useEffect(() => {
    setResumeAttemptId(new URLSearchParams(window.location.search).get("attempt"));
  }, []);

  const startSimulator = useStartSimulator();

  const [attempt, setAttempt] = useState<TestAttemptStarted | null>(null);

  const resumeQuery = useQuery({
    queryKey: ["evaluation-attempt", resumeAttemptId],
    queryFn: () => fetchAttempt(resumeAttemptId!),
    enabled: !!resumeAttemptId && !attempt,
  });

  function handleStart() {
    startSimulator.mutate(undefined, { onSuccess: setAttempt });
  }

  function handleFinished(result: TestResult) {
    router.push(`/results/${result.test_attempt_id}`);
  }

  const activeAttempt = attempt ?? (resumeAttemptId ? resumeQuery.data : null);

  if (activeAttempt) {
    // revealFeedback=false: nunca se muestra si la respuesta fue correcta
    // hasta terminar, tal como se especificó para el Simulador Oficial.
    return <TestRunner attempt={activeAttempt} revealFeedback={false} onFinished={handleFinished} />;
  }

  if (resumeAttemptId && resumeQuery.isLoading) {
    return (
      <div className="p-6">
        <div className="h-6 w-40 animate-pulse rounded bg-surface" />
      </div>
    );
  }

  return (
    <div className="animate-fade-in mx-auto max-w-2xl space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Simulador Oficial</h1>
        <p className="text-sm text-foreground-muted">Replica la experiencia completa del examen oficial de la UPMH.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Información del simulador</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div className="flex items-center gap-3 rounded border border-border p-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded bg-primary/10 text-primary">
              <Clock className="h-5 w-5" />
            </div>
            <div>
              <p className="text-lg font-semibold text-foreground">80 minutos</p>
              <p className="text-xs text-foreground-muted">Duración</p>
            </div>
          </div>
          <div className="flex items-center gap-3 rounded border border-border p-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded bg-accent-green/10 text-accent-green">
              <ClipboardList className="h-5 w-5" />
            </div>
            <div>
              <p className="text-lg font-semibold text-foreground">~90 preguntas</p>
              <p className="text-xs text-foreground-muted">Número de preguntas</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Secciones incluidas</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2.5">
          <div className="flex items-center gap-2.5 text-sm text-foreground">
            <BookOpen className="h-4 w-4 text-foreground-muted" />
            Reading
          </div>
          <div className="flex items-center gap-2.5 text-sm text-foreground">
            <PenSquare className="h-4 w-4 text-foreground-muted" />
            Structure
          </div>
          <div className="flex items-center gap-2.5 text-sm text-foreground">
            <SpellCheck className="h-4 w-4 text-foreground-muted" />
            Written Expression
          </div>
          <div className="flex items-center gap-2.5 text-sm text-foreground-muted">
            <Headphones className="h-4 w-4" />
            Listening
            <Badge variant="secondary">Próximamente</Badge>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base text-warning">
            <AlertTriangle className="h-4 w-4" />
            Antes de comenzar
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-1.5 text-sm text-foreground-muted">
            <li>• No habrá retroalimentación durante el examen.</li>
            <li>• No podrás pausar el simulador.</li>
            <li>• El resultado aparecerá únicamente al finalizar.</li>
            <li>• Debes completar todas las secciones.</li>
          </ul>
        </CardContent>
      </Card>

      <Button className="w-full" onClick={handleStart} disabled={startSimulator.isPending}>
        {startSimulator.isPending ? "Preparando..." : "Iniciar Simulador"}
      </Button>
    </div>
  );
}

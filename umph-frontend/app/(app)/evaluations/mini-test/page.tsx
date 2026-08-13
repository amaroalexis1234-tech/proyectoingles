"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Award, BookOpen, PenSquare, Shuffle } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { fetchAttempt } from "@/features/evaluations/api";
import { TestRunner } from "@/features/evaluations/components/test-runner";
import { useStartMiniTest } from "@/features/evaluations/hooks/use-start-mini-test";
import type { MiniTestMode, TestAttemptStarted, TestResult } from "@/features/evaluations/api";

const MODES: {
  value: MiniTestMode;
  label: string;
  description: string;
  icon: typeof BookOpen;
  color: string;
}[] = [
  { value: "grammar", label: "Grammar", description: "Structure + Written Expression mezclados.", icon: PenSquare, color: "text-primary bg-primary/10" },
  { value: "reading", label: "Reading", description: "Un passage completo con sus preguntas.", icon: BookOpen, color: "text-accent-green bg-accent-green/10" },
  { value: "mixed", label: "Mixed", description: "Grammar + Vocabulary combinados.", icon: Shuffle, color: "text-accent-purple bg-accent-purple/10" },
  { value: "official", label: "Official", description: "Muestra fija de las 4 secciones.", icon: Award, color: "text-accent-orange bg-accent-orange/10" },
];

export default function MiniTestPage() {
  const router = useRouter();
  // Se lee directo de window.location en vez de useSearchParams(): en este
  // entorno, useSearchParams() envuelto en Suspense se queda colgado
  // indefinidamente cuando la URL no trae ningun query param -- este
  // componente es 100% cliente, no necesita el bailout de Suspense.
  const [resumeAttemptId, setResumeAttemptId] = useState<string | null>(null);
  useEffect(() => {
    setResumeAttemptId(new URLSearchParams(window.location.search).get("attempt"));
  }, []);

  const startMiniTest = useStartMiniTest();

  const [attempt, setAttempt] = useState<TestAttemptStarted | null>(null);

  const resumeQuery = useQuery({
    queryKey: ["evaluation-attempt", resumeAttemptId],
    queryFn: () => fetchAttempt(resumeAttemptId!),
    enabled: !!resumeAttemptId && !attempt,
  });

  function handleStart(mode: MiniTestMode) {
    startMiniTest.mutate({ mode }, { onSuccess: setAttempt });
  }

  function handleFinished(result: TestResult) {
    router.push(`/results/${result.test_attempt_id}`);
  }

  const activeAttempt = attempt ?? (resumeAttemptId ? resumeQuery.data : null);

  if (activeAttempt) {
    return <TestRunner attempt={activeAttempt} revealFeedback onFinished={handleFinished} />;
  }

  if (resumeAttemptId && resumeQuery.isLoading) {
    return (
      <div className="p-6">
        <div className="h-6 w-40 animate-pulse rounded bg-surface" />
      </div>
    );
  }

  return (
    <div className="animate-fade-in space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Mini Test</h1>
        <p className="text-sm text-foreground-muted">Practica rápidamente antes del examen.</p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {MODES.map(({ value, label, description, icon: Icon, color }) => (
          <Card key={value} className="flex flex-col">
            <div className={`mb-4 flex h-11 w-11 items-center justify-center rounded ${color}`}>
              <Icon className="h-5 w-5" />
            </div>
            <p className="font-semibold text-foreground">{label}</p>
            <p className="mb-4 flex-1 text-sm text-foreground-muted">{description}</p>
            <Button
              size="sm"
              className="w-full"
              onClick={() => handleStart(value)}
              disabled={startMiniTest.isPending}
            >
              {startMiniTest.isPending ? "Preparando..." : "Seleccionar"}
            </Button>
          </Card>
        ))}
      </div>
    </div>
  );
}

"use client";

import { useState } from "react";
import { CheckCircle2, Sparkles, XCircle } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { AiFeedbackContent } from "@/features/ai/components/ai-feedback-content";
import { useExplainQuestion } from "@/features/ai/hooks/use-explain-question";
import { usePassage } from "@/features/learning/hooks/use-passage";
import { useSubmitAttempt } from "@/features/learning/hooks/use-submit-attempt";
import type { SubmitAttemptResponse } from "@/features/learning/api";
import { cn } from "@/lib/utils";

const OPTION_KEYS = ["A", "B", "C", "D"] as const;

/**
 * Reading tiene su propio componente (no reutiliza ExercisePractice)
 * porque el design system exige panel lateral PERMANENTE junto al
 * passage -- nunca modales que tapen el texto mientras se responde.
 */
export function ReadingPractice({ passageId }: { passageId: string }) {
  const { data: passage, isLoading } = usePassage(passageId);
  const submitAttempt = useSubmitAttempt();
  const explainQuestion = useExplainQuestion();

  const [index, setIndex] = useState(0);
  const [selected, setSelected] = useState<string | null>(null);
  const [result, setResult] = useState<SubmitAttemptResponse | null>(null);
  const [correctCount, setCorrectCount] = useState(0);
  const [startedAt, setStartedAt] = useState(() => Date.now());

  if (isLoading || !passage) {
    return (
      <div className="p-6">
        <div className="h-6 w-40 animate-pulse rounded bg-surface" />
      </div>
    );
  }

  const questions = passage.questions;
  const isFinished = index >= questions.length;
  const current = questions[index];

  function handleSelect(optionKey: string) {
    if (result) return;
    setSelected(optionKey);
    const timeSpent = Math.round((Date.now() - startedAt) / 1000);

    submitAttempt.mutate(
      { question_id: current.id, selected_answer: optionKey, time_spent_seconds: timeSpent },
      {
        onSuccess: (data) => {
          setResult(data);
          if (data.is_correct) setCorrectCount((c) => c + 1);
        },
      }
    );
  }

  function handleNext() {
    setIndex((i) => i + 1);
    setSelected(null);
    setResult(null);
    explainQuestion.reset();
    setStartedAt(Date.now());
  }

  return (
    <div className="animate-fade-in grid h-[calc(100vh-8rem)] grid-cols-1 md:h-[calc(100vh-4rem)] md:grid-cols-[1.3fr_1fr]">
      {/* Panel del passage: siempre visible, nunca se oculta */}
      <div className="overflow-y-auto border-r border-border p-8">
        <h1 className="mb-4 text-xl font-semibold text-foreground">{passage.title}</h1>
        <div className="space-y-4 whitespace-pre-line text-base leading-relaxed text-foreground-muted">
          {passage.text}
        </div>
      </div>

      {/* Panel lateral fijo de preguntas */}
      <div className="overflow-y-auto p-6">
        {isFinished ? (
          <Card className="text-center">
            <CardContent className="space-y-4 pt-2">
              <h2 className="text-lg font-semibold text-foreground">¡Passage completado!</h2>
              <p className="text-foreground-muted">
                {correctCount} de {questions.length} correctas.
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-5">
            <Progress value={((index + (result ? 1 : 0)) / questions.length) * 100} />
            <p className="text-sm text-foreground-muted">
              Pregunta {index + 1} de {questions.length}
            </p>

            <p className="text-base text-foreground">{current.prompt}</p>

            <div className="space-y-2">
              {OPTION_KEYS.filter((key) => current.options[key]).map((key) => {
                const isSelected = selected === key;
                const isCorrectOption = result && key === result.correct_answer;
                const isWrongSelection = result && isSelected && !result.is_correct;

                return (
                  <button
                    key={key}
                    onClick={() => handleSelect(key)}
                    disabled={!!result}
                    className={cn(
                      "flex w-full items-center gap-3 rounded border px-3 py-2.5 text-left text-sm transition-colors",
                      !result && "border-border hover:border-primary hover:bg-primary/5",
                      !result && isSelected && "border-primary bg-primary/5",
                      isCorrectOption && "border-success bg-success/10",
                      isWrongSelection && "border-error bg-error/10",
                      result && !isSelected && !isCorrectOption && "border-border opacity-60"
                    )}
                  >
                    <span className="font-medium text-foreground-muted">{key}</span>
                    <span className="text-foreground">{current.options[key]}</span>
                    {isCorrectOption && <CheckCircle2 className="ml-auto h-4 w-4 text-success" />}
                    {isWrongSelection && <XCircle className="ml-auto h-4 w-4 text-error" />}
                  </button>
                );
              })}
            </div>

            {result && (
              <div className="space-y-3 border-t border-border pt-4">
                <p className={cn("text-sm font-medium", result.is_correct ? "text-success" : "text-error")}>
                  {result.is_correct ? `¡Correcto! +${result.xp_awarded} XP` : "No es correcto."}
                </p>

                {!explainQuestion.data && !explainQuestion.isPending && (
                  <button
                    onClick={() =>
                      explainQuestion.mutate({ questionId: current.id, studentAnswer: selected ?? undefined })
                    }
                    className="flex items-center gap-1.5 text-sm font-medium text-primary hover:underline"
                  >
                    <Sparkles className="h-3.5 w-3.5" />
                    Explicar con IA
                  </button>
                )}

                {(explainQuestion.data || explainQuestion.isPending) && (
                  <div className="rounded border border-primary/30 bg-primary/5 p-3">
                    <AiFeedbackContent
                      data={explainQuestion.data}
                      isLoading={explainQuestion.isPending}
                      isError={explainQuestion.isError}
                      compact
                    />
                  </div>
                )}

                <Button onClick={handleNext} size="sm">
                  {index === questions.length - 1 ? "Ver resultado" : "Siguiente"}
                </Button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

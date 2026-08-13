"use client";

import { useCallback, useMemo, useState } from "react";
import { Clock } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { UnderlinedPrompt } from "@/features/learning/components/underlined-prompt";
import { useCompleteAttempt } from "@/features/evaluations/hooks/use-complete-attempt";
import { useCountdown } from "@/features/evaluations/hooks/use-countdown";
import { useSubmitTestAnswer } from "@/features/evaluations/hooks/use-submit-test-answer";
import type { TestAttemptStarted, TestResult } from "@/features/evaluations/api";
import { cn } from "@/lib/utils";

const OPTION_KEYS = ["A", "B", "C", "D"] as const;

interface TestRunnerProps {
  attempt: TestAttemptStarted;
  /** Mini Test revela si la respuesta fue correcta al momento; Simulador nunca lo hace. */
  revealFeedback: boolean;
  onFinished: (result: TestResult) => void;
}

export function TestRunner({ attempt, revealFeedback, onFinished }: TestRunnerProps) {
  // Al reanudar: arranca en la primera pregunta sin responder (o la
  // ultima, si ya se respondieron todas) en vez de reiniciar en 0.
  const initialIndex = useMemo(() => {
    const firstUnanswered = attempt.items.findIndex((item) => !item.answered);
    return firstUnanswered === -1 ? attempt.items.length - 1 : firstUnanswered;
  }, [attempt.items]);

  const initialAnswers = useMemo(() => {
    const seeded: Record<string, string> = {};
    for (const item of attempt.items) {
      if (item.selected_answer) seeded[item.question.id] = item.selected_answer;
    }
    return seeded;
  }, [attempt.items]);

  // Simulador: el tiempo restante real se calcula desde started_at, no se
  // reinicia el reloj completo al reanudar.
  const remainingSeconds = useMemo(() => {
    if (attempt.time_limit_seconds == null) return null;
    const elapsed = Math.floor((Date.now() - new Date(attempt.started_at).getTime()) / 1000);
    return Math.max(0, attempt.time_limit_seconds - elapsed);
  }, [attempt.time_limit_seconds, attempt.started_at]);

  const [index, setIndex] = useState(initialIndex);
  const [answers, setAnswers] = useState<Record<string, string>>(initialAnswers);
  const [feedback, setFeedback] = useState<{ isCorrect: boolean; correctAnswer: string; explanation: string | null } | null>(null);

  const submitAnswer = useSubmitTestAnswer(attempt.test_attempt_id);
  const completeAttempt = useCompleteAttempt();

  const handleFinish = useCallback(() => {
    completeAttempt.mutate(attempt.test_attempt_id, { onSuccess: onFinished });
  }, [attempt.test_attempt_id, completeAttempt, onFinished]);

  const { formatted, secondsLeft } = useCountdown(remainingSeconds, handleFinish);

  const current = attempt.items[index];
  const passage = useMemo(
    () => attempt.passages.find((p) => p.id === current.question.passage_id) ?? null,
    [attempt.passages, current.question.passage_id]
  );

  function handleSelect(optionKey: string) {
    if (revealFeedback && feedback) return; // Mini Test: ya se vio el feedback, hay que avanzar

    setAnswers((prev) => ({ ...prev, [current.question.id]: optionKey }));

    submitAnswer.mutate(
      { questionId: current.question.id, selectedAnswer: optionKey },
      {
        onSuccess: (data) => {
          if (revealFeedback && data.correct_answer) {
            setFeedback({
              isCorrect: !!data.is_correct,
              correctAnswer: data.correct_answer,
              explanation: data.explanation,
            });
          }
        },
      }
    );
  }

  function goTo(newIndex: number) {
    setIndex(Math.max(0, Math.min(attempt.items.length - 1, newIndex)));
    setFeedback(null);
  }

  const isLast = index === attempt.items.length - 1;
  const selectedForCurrent = answers[current.question.id];

  return (
    <div className={cn("animate-fade-in", passage ? "grid h-[calc(100vh-8rem)] grid-cols-1 md:h-[calc(100vh-4rem)] md:grid-cols-[1.3fr_1fr]" : "p-6")}>
      {passage && (
        <div className="overflow-y-auto border-r border-border p-8">
          <h2 className="mb-4 text-xl font-semibold text-foreground">{passage.title}</h2>
          <div className="whitespace-pre-line text-base leading-relaxed text-foreground-muted">{passage.text}</div>
        </div>
      )}

      <div className={cn("space-y-5", passage ? "overflow-y-auto p-6" : "mx-auto max-w-2xl")}>
        <div className="flex items-center justify-between">
          <p className="text-sm text-foreground-muted">
            Pregunta {index + 1} de {attempt.items.length}
          </p>
          {attempt.time_limit_seconds != null && (
            <span
              className={cn(
                "flex items-center gap-1.5 text-sm font-medium",
                secondsLeft < 60 ? "text-error" : "text-foreground-muted"
              )}
            >
              <Clock className="h-4 w-4" />
              {formatted}
            </span>
          )}
        </div>

        <Progress value={(Object.keys(answers).length / attempt.items.length) * 100} />

        <Card>
          <CardContent className="space-y-4 pt-2">
            {current.question.section === "written_expression" ? (
              <UnderlinedPrompt
                prompt={current.question.prompt}
                options={current.question.options}
                feedback={revealFeedback && feedback ? { correctAnswer: feedback.correctAnswer, selected: selectedForCurrent ?? null } : null}
              />
            ) : (
              <p className="text-base text-foreground">{current.question.prompt}</p>
            )}

            <div className="space-y-2">
              {OPTION_KEYS.filter((key) => current.question.options[key]).map((key) => {
                const isSelected = selectedForCurrent === key;
                const isCorrectOption = revealFeedback && feedback && key === feedback.correctAnswer;
                const isWrongSelection = revealFeedback && feedback && isSelected && !feedback.isCorrect;

                return (
                  <button
                    key={key}
                    onClick={() => handleSelect(key)}
                    disabled={revealFeedback && !!feedback}
                    className={cn(
                      "flex w-full items-center gap-3 rounded border px-4 py-3 text-left text-sm transition-colors",
                      isSelected && !feedback && "border-primary bg-primary/5",
                      !isSelected && !feedback && "border-border hover:border-primary hover:bg-primary/5",
                      isCorrectOption && "border-success bg-success/10",
                      isWrongSelection && "border-error bg-error/10"
                    )}
                  >
                    <span className="font-medium text-foreground-muted">{key}</span>
                    <span className="text-foreground">{current.question.options[key]}</span>
                  </button>
                );
              })}
            </div>

            {revealFeedback && feedback && (
              <div className="space-y-2 border-t border-border pt-4">
                <p className={cn("text-sm font-medium", feedback.isCorrect ? "text-success" : "text-error")}>
                  {feedback.isCorrect ? "¡Correcto!" : "No es correcto."}
                </p>
                {feedback.explanation && <p className="text-sm text-foreground-muted">{feedback.explanation}</p>}
              </div>
            )}
          </CardContent>
        </Card>

        <div className="flex items-center justify-between">
          <Button variant="secondary" size="sm" onClick={() => goTo(index - 1)} disabled={index === 0}>
            Anterior
          </Button>

          {isLast ? (
            <Button size="sm" onClick={handleFinish} disabled={completeAttempt.isPending}>
              Finalizar
            </Button>
          ) : (
            <Button
              size="sm"
              onClick={() => goTo(index + 1)}
              disabled={revealFeedback && !feedback}
            >
              Siguiente
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}

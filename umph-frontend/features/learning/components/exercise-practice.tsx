"use client";

import { useState } from "react";
import { CheckCircle2, XCircle } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useExplainQuestion } from "@/features/ai/hooks/use-explain-question";
import { AiFeedbackOverlay } from "@/features/learning/components/ai-feedback-overlay";
import { UnderlinedPrompt } from "@/features/learning/components/underlined-prompt";
import { useExercises } from "@/features/learning/hooks/use-exercises";
import { XpGainBadge } from "@/features/progress/components/xp-gain-badge";
import { useSubmitAttempt } from "@/features/learning/hooks/use-submit-attempt";
import type { Section, SubmitAttemptResponse } from "@/features/learning/api";
import { cn } from "@/lib/utils";

interface ExercisePracticeProps {
  section: Section;
  title: string;
  description: string;
  /** true para Vocabulary: el prompt trae <u>...</u> y se renderiza como HTML de confianza (contenido propio, no de usuarios). */
  renderPromptAsHtml?: boolean;
}

const OPTION_KEYS = ["A", "B", "C", "D"] as const;

/**
 * Componente generico reutilizado por Structure, Written Expression y
 * Vocabulary -- las tres secciones comparten exactamente el mismo patron
 * de interaccion (pregunta -> 4 opciones -> feedback inmediato -> siguiente).
 * Solo Reading tiene su propio componente por el panel lateral fijo.
 */
export function ExercisePractice({ section, title, description, renderPromptAsHtml }: ExercisePracticeProps) {
  const { data: exercises, isLoading } = useExercises(section, 10);
  const submitAttempt = useSubmitAttempt();
  const explainQuestion = useExplainQuestion();
  const [overlayOpen, setOverlayOpen] = useState(false);

  const [index, setIndex] = useState(0);
  const [selected, setSelected] = useState<string | null>(null);
  const [result, setResult] = useState<SubmitAttemptResponse | null>(null);
  const [correctCount, setCorrectCount] = useState(0);
  const [startedAt, setStartedAt] = useState(() => Date.now());

  if (isLoading || !exercises) {
    return (
      <div className="p-6">
        <div className="h-6 w-40 animate-pulse rounded bg-surface" />
      </div>
    );
  }

  if (exercises.length === 0) {
    return (
      <div className="p-6">
        <p className="text-foreground-muted">Todavía no hay ejercicios cargados para esta sección.</p>
      </div>
    );
  }

  const current = exercises[index];
  const isLastQuestion = index === exercises.length - 1;
  const isFinished = index >= exercises.length;

  function handleSelect(optionKey: string) {
    if (result) return; // ya respondio esta, no permite cambiar tras ver el feedback
    setSelected(optionKey);
    const timeSpent = Math.round((Date.now() - startedAt) / 1000);

    submitAttempt.mutate(
      { question_id: current.id, selected_answer: optionKey, time_spent_seconds: timeSpent },
      {
        onSuccess: (data) => {
          setResult(data);
          if (data.is_correct) setCorrectCount((c) => c + 1);
          setOverlayOpen(true);
          explainQuestion.mutate({ questionId: current.id, studentAnswer: optionKey });
        },
      }
    );
  }

  function handleNext() {
    setIndex((i) => i + 1);
    setSelected(null);
    setResult(null);
    setOverlayOpen(false);
    explainQuestion.reset();
    setStartedAt(Date.now());
  }

  if (isFinished) {
    return (
      <div className="animate-fade-in p-6">
        <Card className="mx-auto max-w-md text-center">
          <CardContent className="space-y-4 pt-2">
            <h2 className="text-xl font-semibold text-foreground">¡Sesión completada!</h2>
            <p className="text-foreground-muted">
              Respondiste correctamente {correctCount} de {exercises.length}.
            </p>
            <Button onClick={() => { setIndex(0); setCorrectCount(0); setResult(null); setSelected(null); setStartedAt(Date.now()); }}>
              Practicar otra vez
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="animate-fade-in space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">{title}</h1>
        <p className="text-sm text-foreground-muted">{description}</p>
      </div>

      <Progress value={((index + (result ? 1 : 0)) / exercises.length) * 100} className="max-w-md" />

      <Card className="max-w-2xl">
        <CardContent className="space-y-5 pt-2">
          {section === "written_expression" ? (
            <UnderlinedPrompt
              prompt={current.prompt}
              options={current.options}
              feedback={result ? { correctAnswer: result.correct_answer, selected } : null}
            />
          ) : renderPromptAsHtml ? (
            <p
              className="text-lg text-foreground"
              dangerouslySetInnerHTML={{ __html: current.prompt }}
            />
          ) : (
            <p className="text-lg text-foreground">{current.prompt}</p>
          )}

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
                    "flex w-full items-center gap-3 rounded border px-4 py-3 text-left text-sm transition-colors",
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
              {result.is_correct ? (
                <div className="flex items-center gap-2">
                  <p className="text-sm font-medium text-success">¡Correcto!</p>
                  <XpGainBadge amount={result.xp_awarded} />
                </div>
              ) : (
                <p className="text-sm font-medium text-error">No es correcto.</p>
              )}
              {result.explanation && <p className="text-sm text-foreground-muted">{result.explanation}</p>}

              {/* Respaldo si el estudiante cierra el overlay sin usar su Continuar. */}
              <Button onClick={handleNext} variant="secondary" size="sm">
                {isLastQuestion ? "Ver resultado" : "Siguiente"}
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      {result && (
        <AiFeedbackOverlay
          open={overlayOpen}
          onOpenChange={setOverlayOpen}
          questionNumber={index + 1}
          totalQuestions={exercises.length}
          result={result}
          aiData={explainQuestion.data}
          aiLoading={explainQuestion.isPending}
          aiError={explainQuestion.isError}
          isLastQuestion={isLastQuestion}
          onContinue={handleNext}
        />
      )}
    </div>
  );
}

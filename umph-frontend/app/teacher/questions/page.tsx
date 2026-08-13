"use client";

import { useState } from "react";
import { Trash2 } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { CreateQuestionDialog } from "@/features/teacher/components/create-question-dialog";
import { ImportQuestionsDialog } from "@/features/teacher/components/import-questions-dialog";
import type { Section } from "@/features/teacher/api";
import { useDeleteQuestion, useQuestions } from "@/features/teacher/hooks/use-question-bank";
import { cn } from "@/lib/utils";

const SECTION_FILTERS: { value: Section | undefined; label: string }[] = [
  { value: undefined, label: "Todas" },
  { value: "structure", label: "Structure" },
  { value: "written_expression", label: "Written Expression" },
  { value: "reading", label: "Reading" },
  { value: "vocabulary", label: "Vocabulary" },
];

export default function TeacherQuestionsPage() {
  const [section, setSection] = useState<Section | undefined>(undefined);
  const { data: questions, isLoading } = useQuestions(section);
  const deleteQuestion = useDeleteQuestion();

  return (
    <div className="animate-fade-in space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-foreground">Banco de preguntas</h1>
          <p className="text-sm text-foreground-muted">
            Las preguntas que crees aquí se integran directo a Mini Tests y al Simulador.
          </p>
        </div>
        <div className="flex gap-2">
          <ImportQuestionsDialog />
          <CreateQuestionDialog />
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        {SECTION_FILTERS.map((f) => (
          <button
            key={f.label}
            onClick={() => setSection(f.value)}
            className={cn(
              "rounded px-3 py-1.5 text-sm font-medium transition-colors",
              section === f.value ? "bg-primary text-primary-foreground" : "bg-surface text-foreground-muted hover:text-foreground"
            )}
          >
            {f.label}
          </button>
        ))}
      </div>

      {isLoading || !questions ? (
        <div className="h-24 animate-pulse rounded bg-surface" />
      ) : questions.length === 0 ? (
        <Card>
          <CardContent className="pt-2 text-sm text-foreground-muted">
            Todavía no hay preguntas en esta sección.
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {questions.map((q) => (
            <Card key={q.id}>
              <CardContent className="flex items-start justify-between gap-4 pt-2">
                <div className="min-w-0">
                  <div className="mb-1 flex items-center gap-2">
                    <Badge variant="secondary">{q.section}</Badge>
                    {q.verified && <Badge variant="success">Verificada</Badge>}
                  </div>
                  <p className="text-sm text-foreground">{q.prompt}</p>
                  <p className="mt-1 text-xs text-foreground-muted">
                    Respuesta correcta: {q.correct_answer} — {q.options[q.correct_answer]}
                  </p>
                  <p className="mt-1 text-xs text-foreground-muted">{q.source}</p>
                </div>
                <button
                  onClick={() => deleteQuestion.mutate(q.id)}
                  disabled={deleteQuestion.isPending}
                  className="flex h-8 w-8 shrink-0 items-center justify-center rounded text-foreground-muted transition-colors hover:bg-error/10 hover:text-error"
                  aria-label="Eliminar pregunta"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

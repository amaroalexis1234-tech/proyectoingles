"use client";

import { useState, type FormEvent } from "react";
import { Plus } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Dialog, DialogCloseButton, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import type { QuestionType, Section } from "@/features/teacher/api";
import { useCreatePassage, useCreateQuestion, usePassages } from "@/features/teacher/hooks/use-question-bank";
import { ApiError } from "@/lib/api-client";
import { cn } from "@/lib/utils";

const SECTIONS: { value: Section; label: string; questionType: QuestionType }[] = [
  { value: "structure", label: "Structure", questionType: "sentence_completion" },
  { value: "written_expression", label: "Written Expression", questionType: "error_identification" },
  { value: "reading", label: "Reading", questionType: "multiple_choice" },
  { value: "vocabulary", label: "Vocabulary", questionType: "vocabulary_choice" },
];

const OPTION_KEYS = ["A", "B", "C", "D"] as const;

export function CreateQuestionDialog() {
  const { data: passages } = usePassages();
  const createQuestion = useCreateQuestion();
  const createPassage = useCreatePassage();

  const [open, setOpen] = useState(false);
  const [section, setSection] = useState<Section>("structure");
  const [prompt, setPrompt] = useState("");
  const [options, setOptions] = useState({ A: "", B: "", C: "", D: "" });
  const [correctAnswer, setCorrectAnswer] = useState<string>("A");
  const [explanation, setExplanation] = useState("");
  const [passageMode, setPassageMode] = useState<"existing" | "new">("existing");
  const [selectedPassageId, setSelectedPassageId] = useState("");
  const [newPassage, setNewPassage] = useState({ title: "", text: "", source: "" });
  const [formError, setFormError] = useState<string | null>(null);

  const isSaving = createQuestion.isPending || createPassage.isPending;

  function reset() {
    setSection("structure");
    setPrompt("");
    setOptions({ A: "", B: "", C: "", D: "" });
    setCorrectAnswer("A");
    setExplanation("");
    setPassageMode("existing");
    setSelectedPassageId("");
    setNewPassage({ title: "", text: "", source: "" });
    setFormError(null);
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setFormError(null);

    try {
      let passageId: string | undefined;

      if (section === "reading") {
        if (passageMode === "existing") {
          if (!selectedPassageId) {
            setFormError("Selecciona un passage.");
            return;
          }
          passageId = selectedPassageId;
        } else {
          const passage = await createPassage.mutateAsync(newPassage);
          passageId = passage.id;
        }
      }

      const questionType = SECTIONS.find((s) => s.value === section)!.questionType;
      await createQuestion.mutateAsync({
        section,
        question_type: questionType,
        prompt,
        options,
        correct_answer: correctAnswer,
        explanation: explanation || undefined,
        passage_id: passageId,
      });

      setOpen(false);
      reset();
    } catch (error) {
      setFormError(error instanceof ApiError ? error.message : "No se pudo crear la pregunta. Intenta de nuevo.");
    }
  }

  return (
    <Dialog
      open={open}
      onOpenChange={(next) => {
        setOpen(next);
        if (next) reset();
      }}
    >
      <DialogTrigger asChild>
        <Button size="sm">
          <Plus className="h-4 w-4" />
          Crear pregunta
        </Button>
      </DialogTrigger>
      <DialogContent className="flex items-start justify-center overflow-y-auto bg-transparent p-4 sm:items-center">
        <div className="w-full max-w-lg rounded border border-border bg-surface p-6 shadow-card">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-foreground">Crear pregunta</h2>
            <DialogCloseButton />
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label>Sección</Label>
              <div className="grid grid-cols-2 gap-2">
                {SECTIONS.map((s) => (
                  <button
                    key={s.value}
                    type="button"
                    onClick={() => setSection(s.value)}
                    className={cn(
                      "rounded border px-3 py-2 text-sm transition-colors",
                      section === s.value ? "border-primary bg-primary/5 text-primary" : "border-border text-foreground-muted hover:border-primary"
                    )}
                  >
                    {s.label}
                  </button>
                ))}
              </div>
            </div>

            {section === "reading" && (
              <div className="space-y-2 rounded border border-border p-3">
                <Label>Passage</Label>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setPassageMode("existing")}
                    className={cn("rounded px-3 py-1.5 text-xs", passageMode === "existing" ? "bg-primary text-primary-foreground" : "bg-background text-foreground-muted")}
                  >
                    Usar existente
                  </button>
                  <button
                    type="button"
                    onClick={() => setPassageMode("new")}
                    className={cn("rounded px-3 py-1.5 text-xs", passageMode === "new" ? "bg-primary text-primary-foreground" : "bg-background text-foreground-muted")}
                  >
                    Crear nuevo
                  </button>
                </div>

                {passageMode === "existing" ? (
                  <select
                    value={selectedPassageId}
                    onChange={(e) => setSelectedPassageId(e.target.value)}
                    className="w-full rounded border border-border bg-background px-3 py-2 text-sm text-foreground"
                  >
                    <option value="">Selecciona un passage...</option>
                    {passages?.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.title ?? p.source}
                      </option>
                    ))}
                  </select>
                ) : (
                  <div className="space-y-2">
                    <Input
                      placeholder="Título (opcional)"
                      value={newPassage.title}
                      onChange={(e) => setNewPassage((p) => ({ ...p, title: e.target.value }))}
                    />
                    <textarea
                      required
                      placeholder="Texto completo del passage"
                      value={newPassage.text}
                      onChange={(e) => setNewPassage((p) => ({ ...p, text: e.target.value }))}
                      rows={4}
                      className="flex w-full rounded border border-border bg-background px-4 py-2 text-sm text-foreground placeholder:text-foreground-muted"
                    />
                    <Input
                      required
                      placeholder="Fuente (ej. Examen propio - Unidad 3)"
                      value={newPassage.source}
                      onChange={(e) => setNewPassage((p) => ({ ...p, source: e.target.value }))}
                    />
                  </div>
                )}
              </div>
            )}

            <div className="space-y-2">
              <Label htmlFor="prompt">Pregunta</Label>
              <textarea
                id="prompt"
                required
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                rows={2}
                className="flex w-full rounded border border-border bg-background px-4 py-2 text-sm text-foreground placeholder:text-foreground-muted"
              />
            </div>

            <div className="space-y-2">
              <Label>Opciones</Label>
              {OPTION_KEYS.map((key) => (
                <div key={key} className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => setCorrectAnswer(key)}
                    title="Marcar como correcta"
                    className={cn(
                      "flex h-8 w-8 shrink-0 items-center justify-center rounded-full border text-xs font-semibold",
                      correctAnswer === key ? "border-success bg-success/10 text-success" : "border-border text-foreground-muted"
                    )}
                  >
                    {key}
                  </button>
                  <Input
                    required
                    placeholder={`Opción ${key}`}
                    value={options[key]}
                    onChange={(e) => setOptions((o) => ({ ...o, [key]: e.target.value }))}
                  />
                </div>
              ))}
              <p className="text-xs text-foreground-muted">Haz click en la letra para marcar la respuesta correcta.</p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="explanation">Explicación (opcional)</Label>
              <textarea
                id="explanation"
                value={explanation}
                onChange={(e) => setExplanation(e.target.value)}
                rows={2}
                className="flex w-full rounded border border-border bg-background px-4 py-2 text-sm text-foreground placeholder:text-foreground-muted"
              />
            </div>

            {formError && (
              <p role="alert" className="text-sm text-error">
                {formError}
              </p>
            )}

            <Button type="submit" className="w-full" disabled={isSaving}>
              {isSaving ? "Guardando..." : "Crear pregunta"}
            </Button>
          </form>
        </div>
      </DialogContent>
    </Dialog>
  );
}

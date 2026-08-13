"use client";

import { useRef, useState, type ChangeEvent } from "react";
import { Download, Upload } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Dialog, DialogCloseButton, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import type { QuestionImportResult } from "@/features/teacher/api";
import { useImportQuestionsCsv } from "@/features/teacher/hooks/use-question-bank";
import { ApiError } from "@/lib/api-client";

const CSV_TEMPLATE =
  "section,question_type,prompt,option_a,option_b,option_c,option_d,correct_answer,explanation,passage_title\n" +
  'structure,sentence_completion,"Coffee probably originally grew wild in Ethiopia and from there ___ to southern Arabia.",was spread,spread,spreading,to spread,B,"Se necesita el verbo principal en pasado simple.",\n';

function downloadTemplate() {
  const blob = new Blob([CSV_TEMPLATE], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "plantilla-preguntas.csv";
  link.click();
  URL.revokeObjectURL(url);
}

export function ImportQuestionsDialog() {
  const importQuestions = useImportQuestionsCsv();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [open, setOpen] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [result, setResult] = useState<QuestionImportResult | null>(null);

  function reset() {
    setFileName(null);
    setFormError(null);
    setResult(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  }

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    setFormError(null);
    setResult(null);

    importQuestions.mutate(file, {
      onSuccess: (data) => setResult(data),
      onError: (error) => {
        setFormError(error instanceof ApiError ? error.message : "No se pudo importar el archivo. Intenta de nuevo.");
      },
    });
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
        <Button size="sm" variant="secondary">
          <Upload className="h-4 w-4" />
          Importar CSV
        </Button>
      </DialogTrigger>
      <DialogContent className="flex items-start justify-center overflow-y-auto bg-transparent p-4 sm:items-center">
        <div className="w-full max-w-lg rounded border border-border bg-surface p-6 shadow-card">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-foreground">Importar preguntas por CSV</h2>
            <DialogCloseButton />
          </div>

          <div className="space-y-4">
            <div className="space-y-2 text-sm text-foreground-muted">
              <p>
                Sube un archivo CSV con una pregunta por fila. Cada fila crea una pregunta directo en el banco
                (verificada, igual que las que creas a mano).
              </p>
              <button
                type="button"
                onClick={downloadTemplate}
                className="flex items-center gap-1.5 font-medium text-primary hover:underline"
              >
                <Download className="h-3.5 w-3.5" />
                Descargar plantilla CSV
              </button>
              <p className="text-xs">
                Columnas: <code>section, question_type, prompt, option_a-d, correct_answer</code> (requeridas),{" "}
                <code>explanation, passage_title</code> (opcionales — <code>passage_title</code> debe coincidir con
                un passage ya creado).
              </p>
            </div>

            <div>
              <input
                ref={fileInputRef}
                type="file"
                accept=".csv,text/csv"
                onChange={handleFileChange}
                className="hidden"
              />
              <Button
                type="button"
                disabled={importQuestions.isPending}
                className="w-full"
                onClick={() => fileInputRef.current?.click()}
              >
                {importQuestions.isPending ? "Importando..." : (fileName ?? "Elegir archivo CSV")}
              </Button>
            </div>

            {formError && (
              <p role="alert" className="text-sm text-error">
                {formError}
              </p>
            )}

            {result && (
              <div className="space-y-3 rounded border border-border p-3">
                <div className="flex items-center gap-2">
                  <Badge variant={result.created > 0 ? "success" : "secondary"}>
                    {result.created} pregunta{result.created === 1 ? "" : "s"} creada{result.created === 1 ? "" : "s"}
                  </Badge>
                  {result.errors.length > 0 && (
                    <Badge variant="warning">
                      {result.errors.length} fila{result.errors.length === 1 ? "" : "s"} con error
                    </Badge>
                  )}
                </div>

                {result.errors.length > 0 && (
                  <ul className="max-h-48 space-y-1 overflow-y-auto text-xs">
                    {result.errors.map((e) => (
                      <li key={e.row} className="text-foreground-muted">
                        <span className="font-medium text-error">Fila {e.row}:</span> {e.message}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

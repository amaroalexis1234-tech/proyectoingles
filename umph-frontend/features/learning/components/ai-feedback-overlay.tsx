import { CheckCircle2, XCircle } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Dialog, DialogCloseButton, DialogContent } from "@/components/ui/dialog";
import { AiFeedbackContent } from "@/features/ai/components/ai-feedback-content";
import type { ExplainResponse } from "@/features/ai/api";
import type { SubmitAttemptResponse } from "@/features/learning/api";
import { XpGainBadge } from "@/features/progress/components/xp-gain-badge";
import { cn } from "@/lib/utils";

interface AiFeedbackOverlayProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  questionNumber: number;
  totalQuestions: number;
  result: SubmitAttemptResponse;
  aiData: ExplainResponse | undefined;
  aiLoading: boolean;
  aiError: boolean;
  isLastQuestion: boolean;
  onContinue: () => void;
}

export function AiFeedbackOverlay({
  open,
  onOpenChange,
  questionNumber,
  totalQuestions,
  result,
  aiData,
  aiLoading,
  aiError,
  isLastQuestion,
  onContinue,
}: AiFeedbackOverlayProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <div className="mx-auto flex h-full max-w-2xl flex-col p-6">
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-foreground">Retroalimentación de IA</h2>
              <p className="text-sm text-foreground-muted">
                Pregunta {questionNumber} de {totalQuestions}
              </p>
            </div>
            <DialogCloseButton />
          </div>

          <div
            className={cn(
              "mb-6 flex items-center gap-3 rounded border p-4",
              result.is_correct ? "border-success/40 bg-success/10" : "border-error/40 bg-error/10"
            )}
          >
            {result.is_correct ? (
              <CheckCircle2 className="h-6 w-6 shrink-0 text-success" />
            ) : (
              <XCircle className="h-6 w-6 shrink-0 text-error" />
            )}
            <div>
              <div className="flex items-center gap-2">
                <p className={cn("font-medium", result.is_correct ? "text-success" : "text-error")}>
                  {result.is_correct ? `¡Correcto!` : "No es correcto."}
                </p>
                {result.is_correct && <XpGainBadge amount={result.xp_awarded} />}
              </div>
              {!result.is_correct && (
                <p className="text-sm text-foreground-muted">
                  La respuesta correcta era {result.correct_answer}.
                </p>
              )}
            </div>
          </div>

          <div className="flex-1 overflow-y-auto">
            <AiFeedbackContent data={aiData} isLoading={aiLoading} isError={aiError} />
          </div>

          <Button onClick={onContinue} className="mt-6 w-full">
            {isLastQuestion ? "Ver resultado" : "Continuar"}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}

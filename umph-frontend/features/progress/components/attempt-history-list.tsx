import Link from "next/link";
import { ClipboardCheck, Timer } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import type { TestAttemptSummary } from "@/features/progress/api";
import { cn } from "@/lib/utils";

const MODE_LABELS: Record<string, string> = {
  grammar: "Grammar",
  reading: "Reading",
  mixed: "Mixed",
  official: "Official",
};

/**
 * Extraido de lo que antes vivia dentro de stats/page.tsx -- misma UI,
 * ahora reutilizable (usada por Historial).
 */
interface AttemptHistoryListProps {
  attempts: TestAttemptSummary[];
  // false en la vista de maestro: /results/{id} solo permite ver el dueño
  // real del intento, un maestro entraria a un 403.
  linkToResults?: boolean;
}

export function AttemptHistoryList({ attempts, linkToResults = true }: AttemptHistoryListProps) {
  if (attempts.length === 0) {
    return (
      <Card>
        <CardContent className="pt-2 text-sm text-foreground-muted">
          Todavía no completaste ningún Mini Test ni Simulador. Ve a{" "}
          <span className="text-primary">Evaluaciones</span> para empezar.
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-3">
      {attempts.map((attempt) => {
        const card = (
          <Card className={cn(linkToResults && "transition-colors hover:border-primary")}>
            <CardContent className="flex items-center justify-between pt-2">
              <div className="flex items-center gap-3">
                {attempt.test_type === "simulator" ? (
                  <Timer className="h-5 w-5 text-primary" />
                ) : (
                  <ClipboardCheck className="h-5 w-5 text-primary" />
                )}
                <div>
                  <p className="text-sm font-medium text-foreground">
                    {attempt.test_type === "simulator"
                      ? "Simulador Oficial"
                      : `Mini Test — ${MODE_LABELS[attempt.mini_test_mode ?? ""] ?? attempt.mini_test_mode}`}
                  </p>
                  <p className="text-xs text-foreground-muted">
                    {new Date(attempt.completed_at).toLocaleDateString("es-MX", {
                      day: "numeric",
                      month: "short",
                      year: "numeric",
                    })}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className={cn("text-lg font-semibold", attempt.accuracy >= 70 ? "text-success" : "text-error")}>
                  {attempt.accuracy}%
                </p>
                <p className="text-xs text-foreground-muted">
                  {attempt.correct_count}/{attempt.total_questions}
                </p>
              </div>
            </CardContent>
          </Card>
        );

        return linkToResults ? (
          <Link key={attempt.id} href={`/results/${attempt.id}`}>
            {card}
          </Link>
        ) : (
          <div key={attempt.id}>{card}</div>
        );
      })}
    </div>
  );
}

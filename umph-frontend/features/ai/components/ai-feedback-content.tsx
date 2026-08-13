import { BookOpenCheck, Globe, Quote, Sparkles } from "lucide-react";

import type { ExplainResponse } from "@/features/ai/api";
import { cn } from "@/lib/utils";

interface AiFeedbackContentProps {
  data: ExplainResponse | undefined;
  isLoading: boolean;
  isError: boolean;
  /** Espaciado/tipografia mas apretados para el panel lateral de Reading (~40% de ancho). */
  compact?: boolean;
}

/**
 * Componente presentacional compartido por el overlay de ejercicios y el
 * panel lateral de Reading -- una sola implementacion del render de las
 * secciones de IA. Cada seccion es condicional: nunca se fabrica contenido
 * que el backend no devolvio (evidencia/vocabulario/regla/traduccion
 * quedan null cuando source="fallback").
 */
export function AiFeedbackContent({ data, isLoading, isError, compact }: AiFeedbackContentProps) {
  const gap = compact ? "space-y-3" : "space-y-4";
  const textSize = compact ? "text-sm" : "text-base";

  if (isLoading) {
    return (
      <div className={gap}>
        <div className="h-4 w-3/4 animate-pulse rounded bg-surface" />
        <div className="h-4 w-1/2 animate-pulse rounded bg-surface" />
      </div>
    );
  }

  if (isError || !data) {
    return <p className="text-sm text-foreground-muted">No se pudo obtener la explicación.</p>;
  }

  return (
    <div className={gap}>
      <div>
        <p className="mb-1 flex items-center gap-1.5 text-sm font-medium text-primary">
          <Sparkles className="h-3.5 w-3.5" />
          {data.source === "ai" ? "Explicación con IA" : "Explicación base"}
        </p>
        <p className={cn("text-foreground", textSize)}>{data.explanation}</p>
        {data.source === "fallback" && (
          <p className="mt-1 text-xs text-foreground-muted">IA no disponible en este momento.</p>
        )}
      </div>

      {data.evidence && (
        <div className="rounded border border-border bg-surface p-3">
          <p className="mb-1 flex items-center gap-1.5 text-sm font-medium text-foreground">
            <Quote className="h-3.5 w-3.5 text-foreground-muted" />
            Evidencia en el texto
          </p>
          <p className={cn("italic text-foreground-muted", compact ? "text-xs" : "text-sm")}>
            &ldquo;{data.evidence}&rdquo;
          </p>
        </div>
      )}

      {data.vocabulary_terms && data.vocabulary_terms.length > 0 && (
        <div>
          <p className="mb-1.5 flex items-center gap-1.5 text-sm font-medium text-foreground">
            <BookOpenCheck className="h-3.5 w-3.5 text-foreground-muted" />
            Vocabulario clave
          </p>
          <ul className="space-y-1">
            {data.vocabulary_terms.map((term) => (
              <li key={term.term} className="flex items-baseline gap-2 text-sm">
                <span className="font-medium text-foreground">{term.term}</span>
                <span className="text-foreground-muted">{term.translation}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {data.grammar_rule && (
        <div>
          <p className="mb-1 text-sm font-medium text-foreground">Regla gramatical</p>
          <p className={cn("text-foreground-muted", compact ? "text-xs" : "text-sm")}>{data.grammar_rule}</p>
        </div>
      )}

      {data.translation && (
        <div>
          <p className="mb-1 flex items-center gap-1.5 text-sm font-medium text-foreground">
            <Globe className="h-3.5 w-3.5 text-foreground-muted" />
            En palabras más simples
          </p>
          <p className={cn("text-foreground-muted", compact ? "text-xs" : "text-sm")}>{data.translation}</p>
        </div>
      )}
    </div>
  );
}

import { cn } from "@/lib/utils";

interface UnderlinedPromptProps {
  prompt: string;
  options: Record<string, string>;
  /** Cuando ya hay feedback, colorea el segmento correcto/el elegido incorrecto. */
  feedback?: { correctAnswer: string; selected: string | null } | null;
}

interface Segment {
  type: "text" | "option";
  content: string;
  key?: string;
}

/**
 * En Written Expression cada opcion (A-D) es un segmento literal dentro del
 * prompt (la oracion completa) -- se busca cada uno por substring y se
 * subraya en su posicion real, en vez de solo listarlo aparte sin marcar
 * donde vive dentro de la oracion.
 */
function buildSegments(prompt: string, options: Record<string, string>): Segment[] {
  const matches = Object.entries(options)
    .filter(([, text]) => !!text)
    .map(([key, text]) => ({ key, text, start: prompt.indexOf(text) }))
    .filter((m) => m.start !== -1)
    .sort((a, b) => a.start - b.start);

  const segments: Segment[] = [];
  let cursor = 0;
  for (const m of matches) {
    if (m.start > cursor) segments.push({ type: "text", content: prompt.slice(cursor, m.start) });
    segments.push({ type: "option", content: m.text, key: m.key });
    cursor = m.start + m.text.length;
  }
  if (cursor < prompt.length) segments.push({ type: "text", content: prompt.slice(cursor) });

  // Si no se pudo ubicar ningun segmento (datos que no siguen el formato
  // de substring exacto), se devuelve el prompt completo tal cual.
  return segments.length > 0 ? segments : [{ type: "text", content: prompt }];
}

export function UnderlinedPrompt({ prompt, options, feedback }: UnderlinedPromptProps) {
  const segments = buildSegments(prompt, options);

  return (
    <p className="text-lg text-foreground">
      {segments.map((segment, index) => {
        if (segment.type === "text") {
          return <span key={index}>{segment.content}</span>;
        }

        const isCorrect = feedback && segment.key === feedback.correctAnswer;
        const isWrongSelection = feedback && segment.key === feedback.selected && segment.key !== feedback.correctAnswer;

        return (
          <span
            key={index}
            className={cn(
              "underline decoration-2 underline-offset-4",
              isCorrect && "decoration-success text-success",
              isWrongSelection && "decoration-error text-error",
              !feedback && "decoration-primary"
            )}
          >
            {segment.content}
            <sup className="ml-0.5 text-xs font-semibold text-foreground-muted">({segment.key})</sup>
          </span>
        );
      })}
    </p>
  );
}

interface AccuracyDonutProps {
  correct: number;
  incorrect: number;
  unanswered: number;
  label?: string;
}

const SIZE = 160;
const STROKE = 16;
const RADIUS = (SIZE - STROKE) / 2;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

const SEGMENTS = [
  { key: "correct" as const, label: "Correctas", colorVar: "var(--success)", className: "text-success" },
  { key: "incorrect" as const, label: "Incorrectas", colorVar: "var(--error)", className: "text-error" },
  { key: "unanswered" as const, label: "Sin responder", colorVar: "var(--text-secondary)", className: "text-foreground-muted" },
];

/**
 * SVG hecho a mano (sin libreria de graficas), mismo criterio que
 * progress-chart.tsx. Los 3 segmentos siempre sumar 100% de un total real
 * (correctas + incorrectas + sin responder), nunca datos inventados.
 */
export function AccuracyDonut({ correct, incorrect, unanswered, label = "Precisión" }: AccuracyDonutProps) {
  const total = correct + incorrect + unanswered;

  if (total === 0) {
    return (
      <div className="flex flex-col items-center justify-center gap-2 py-8 text-center">
        <p className="text-sm text-foreground-muted">Aún no hay suficiente actividad para mostrar tu precisión.</p>
      </div>
    );
  }

  const counts = { correct, incorrect, unanswered };
  let offset = 0;
  const arcs = SEGMENTS.map((segment) => {
    const value = counts[segment.key];
    const fraction = value / total;
    const length = fraction * CIRCUMFERENCE;
    const arc = { ...segment, value, percent: Math.round(fraction * 100), length, offset };
    offset += length;
    return arc;
  });

  const precisionPercent = Math.round((correct / total) * 100);

  return (
    <div className="flex flex-col items-center gap-4 sm:flex-row sm:items-center sm:gap-6">
      <svg width={SIZE} height={SIZE} viewBox={`0 0 ${SIZE} ${SIZE}`} className="-rotate-90">
        <circle cx={SIZE / 2} cy={SIZE / 2} r={RADIUS} fill="none" className="stroke-border" strokeWidth={STROKE} />
        {arcs.map((arc) => (
          <circle
            key={arc.key}
            cx={SIZE / 2}
            cy={SIZE / 2}
            r={RADIUS}
            fill="none"
            stroke={arc.colorVar}
            strokeWidth={STROKE}
            strokeDasharray={`${arc.length} ${CIRCUMFERENCE - arc.length}`}
            strokeDashoffset={-arc.offset}
            strokeLinecap="butt"
          />
        ))}
        <text
          x={SIZE / 2}
          y={SIZE / 2}
          textAnchor="middle"
          dominantBaseline="central"
          className="rotate-90 fill-foreground text-2xl font-semibold"
          style={{ transformOrigin: "center", transformBox: "fill-box" }}
        >
          {precisionPercent}%
        </text>
      </svg>

      <div className="space-y-2">
        <p className="text-sm text-foreground-muted">{label}</p>
        {arcs.map((arc) => (
          <div key={arc.key} className="flex items-center gap-2 text-sm">
            <span className={`h-2.5 w-2.5 rounded-full ${arc.className}`} style={{ backgroundColor: "currentColor" }} />
            <span className="text-foreground-muted">{arc.label}</span>
            <span className="font-medium text-foreground">{arc.percent}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}

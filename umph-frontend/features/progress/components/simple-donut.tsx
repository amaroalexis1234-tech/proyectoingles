const SIZE = 160;
const STROKE = 14;
const RADIUS = (SIZE - STROKE) / 2;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

interface SimpleDonutProps {
  percent: number;
  label: string;
}

/** Donut de un solo valor (ej. calificación de un examen) -- SVG hecho a mano. */
export function SimpleDonut({ percent, label }: SimpleDonutProps) {
  const clamped = Math.max(0, Math.min(100, percent));
  const length = (clamped / 100) * CIRCUMFERENCE;
  const colorClass = clamped >= 70 ? "stroke-success" : "stroke-warning";

  return (
    <svg width={SIZE} height={SIZE} viewBox={`0 0 ${SIZE} ${SIZE}`} className="-rotate-90">
      <circle cx={SIZE / 2} cy={SIZE / 2} r={RADIUS} fill="none" className="stroke-border" strokeWidth={STROKE} />
      <circle
        cx={SIZE / 2}
        cy={SIZE / 2}
        r={RADIUS}
        fill="none"
        className={colorClass}
        strokeWidth={STROKE}
        strokeDasharray={`${length} ${CIRCUMFERENCE - length}`}
        strokeLinecap="round"
      />
      <text
        x={SIZE / 2}
        y={SIZE / 2 - 8}
        textAnchor="middle"
        dominantBaseline="central"
        className="rotate-90 fill-foreground text-3xl font-semibold"
        style={{ transformOrigin: "center", transformBox: "fill-box" }}
      >
        {clamped}%
      </text>
      <text
        x={SIZE / 2}
        y={SIZE / 2 + 18}
        textAnchor="middle"
        dominantBaseline="central"
        className="rotate-90 fill-foreground-muted text-xs"
        style={{ transformOrigin: "center", transformBox: "fill-box" }}
      >
        {label}
      </text>
    </svg>
  );
}

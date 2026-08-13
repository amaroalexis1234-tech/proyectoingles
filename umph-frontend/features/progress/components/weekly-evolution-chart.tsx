"use client";

import { useWeeklyEvolution } from "@/features/progress/hooks/use-weekly-evolution";

const WIDTH = 600;
const HEIGHT = 160;
const PADDING = 24;

/**
 * Lun-Dom de la semana en curso. Dias sin actividad (incluye dias futuros)
 * no dibujan punto -- nunca se fabrica un 0%, pero la linea SI conecta
 * los dias que si tienen dato real, aunque no sean consecutivos, para que
 * se lea como una evolucion en vez de puntos sueltos.
 */
export function WeeklyEvolutionChart() {
  const { data: days, isLoading } = useWeeklyEvolution();

  if (isLoading || !days) {
    return <div className="h-40 animate-pulse rounded bg-surface" />;
  }

  const stepX = (WIDTH - PADDING * 2) / (days.length - 1);
  const points = days.map((day, index) => {
    const x = PADDING + index * stepX;
    const y =
      day.accuracy_percent != null ? PADDING + (1 - day.accuracy_percent / 100) * (HEIGHT - PADDING * 2) : null;
    return { ...day, x, y };
  });

  const pointsWithData = points.filter((p) => p.y != null);
  const hasAnyData = pointsWithData.length > 0;

  // La linea conecta todos los dias CON dato real, aunque no sean
  // consecutivos (ej. Lun y Jue) -- se salta los huecos sin fabricar un
  // valor para ellos, en vez de cortar el trazo en cada dia sin actividad.
  const path = pointsWithData.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.y}`).join(" ");

  return (
    <div>
      <svg viewBox={`0 0 ${WIDTH} ${HEIGHT}`} className="w-full" role="img" aria-label="Evolución semanal">
        <line x1={PADDING} y1={HEIGHT - PADDING} x2={WIDTH - PADDING} y2={HEIGHT - PADDING} className="stroke-border" strokeWidth={1} />
        {!hasAnyData ? (
          <text x={WIDTH / 2} y={HEIGHT / 2} textAnchor="middle" className="fill-foreground-muted text-xs">
            Sin actividad esta semana todavía.
          </text>
        ) : (
          <>
            {pointsWithData.length > 1 && <path d={path} fill="none" className="stroke-primary" strokeWidth={2} />}
            {pointsWithData.map((p) => (
              <circle key={p.day_label} cx={p.x} cy={p.y!} r={3.5} className="fill-primary" />
            ))}
          </>
        )}
        {points.map((p) => (
          <text key={p.day_label} x={p.x} y={HEIGHT - PADDING + 14} textAnchor="middle" className="fill-foreground-muted text-[10px]">
            {p.day_label}
          </text>
        ))}
      </svg>
    </div>
  );
}

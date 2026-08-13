"use client";

import { useHistory } from "@/features/progress/hooks/use-history";

const WIDTH = 320;
const HEIGHT = 160;
const PADDING = 24;
const BAR_GAP = 12;

/**
 * Barras de los ultimos 5 examenes -- misma fuente de datos que
 * progress-chart.tsx (usada en el Dashboard), forma visual distinta.
 */
export function RecentExamsChart() {
  const { data: history, isLoading } = useHistory();

  if (isLoading) {
    return <div className="h-40 animate-pulse rounded bg-surface" />;
  }

  const attempts = (history ?? []).slice(0, 5).reverse();

  if (attempts.length === 0) {
    return <p className="text-sm text-foreground-muted">Aún no hay exámenes completados.</p>;
  }

  const innerWidth = WIDTH - PADDING * 2;
  const barWidth = (innerWidth - BAR_GAP * (attempts.length - 1)) / attempts.length;

  return (
    <div>
      <svg viewBox={`0 0 ${WIDTH} ${HEIGHT}`} className="w-full" role="img" aria-label="Últimos exámenes">
        <line x1={PADDING} y1={HEIGHT - PADDING} x2={WIDTH - PADDING} y2={HEIGHT - PADDING} className="stroke-border" strokeWidth={1} />
        {attempts.map((attempt, index) => {
          const barHeight = (attempt.accuracy / 100) * (HEIGHT - PADDING * 2);
          const x = PADDING + index * (barWidth + BAR_GAP);
          const y = HEIGHT - PADDING - barHeight;
          return (
            <g key={attempt.id}>
              <rect x={x} y={y} width={barWidth} height={barHeight} rx={3} className="fill-primary" />
              <text x={x + barWidth / 2} y={y - 6} textAnchor="middle" className="fill-foreground-muted text-[10px]">
                {attempt.accuracy}%
              </text>
              <text x={x + barWidth / 2} y={HEIGHT - PADDING + 14} textAnchor="middle" className="fill-foreground-muted text-[10px]">
                Examen {index + 1}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

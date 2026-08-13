"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useHistory } from "@/features/progress/hooks/use-history";

const WIDTH = 600;
const HEIGHT = 160;
const PADDING = 24;

const MODE_LABELS: Record<string, string> = {
  grammar: "Grammar",
  reading: "Reading",
  mixed: "Mixed",
  official: "Official",
};

/**
 * SVG hecho a mano (sin libreria de graficas nueva) -- solo ~8 puntos de
 * datos, consistente con que Progress ya es hand-rolled en el design
 * system. Usa el endpoint /progress/history ya existente.
 */
export function ProgressChart() {
  const { data: history, isLoading } = useHistory();

  if (isLoading) {
    return <div className="h-48 animate-pulse rounded bg-surface" />;
  }

  const attempts = (history ?? []).slice(0, 8).reverse();

  if (attempts.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Progress</CardTitle>
          <CardDescription>Tu desempeño a lo largo del tiempo.</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-foreground-muted">
            Completa un mini test o el simulador para empezar a ver tu progreso aquí.
          </p>
        </CardContent>
      </Card>
    );
  }

  const stepX = attempts.length > 1 ? (WIDTH - PADDING * 2) / (attempts.length - 1) : 0;
  const points = attempts.map((attempt, index) => {
    const x = PADDING + index * stepX;
    const y = PADDING + (1 - attempt.accuracy / 100) * (HEIGHT - PADDING * 2);
    return { x, y, attempt };
  });
  const path = points.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.y}`).join(" ");

  const latest = attempts[attempts.length - 1];
  const latestLabel =
    latest.test_type === "simulator" ? "Simulador" : MODE_LABELS[latest.mini_test_mode ?? ""] ?? "Mini Test";

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Progress</CardTitle>
        <CardDescription>Tu desempeño a lo largo del tiempo.</CardDescription>
      </CardHeader>
      <CardContent>
        <svg viewBox={`0 0 ${WIDTH} ${HEIGHT}`} className="w-full" role="img" aria-label="Progreso reciente">
          <line x1={PADDING} y1={HEIGHT - PADDING} x2={WIDTH - PADDING} y2={HEIGHT - PADDING} className="stroke-border" strokeWidth={1} />
          <path d={path} fill="none" className="stroke-primary" strokeWidth={2} />
          {points.map((p, i) => (
            <circle key={i} cx={p.x} cy={p.y} r={3.5} className="fill-primary" />
          ))}
        </svg>

        <div className="mt-4 flex items-center justify-between rounded border border-border px-3 py-2.5 text-sm">
          <span className="text-foreground-muted">
            Último resultado — {latestLabel}
          </span>
          <span className={latest.accuracy >= 70 ? "font-semibold text-success" : "font-semibold text-warning"}>
            {latest.accuracy}%
          </span>
        </div>
      </CardContent>
    </Card>
  );
}

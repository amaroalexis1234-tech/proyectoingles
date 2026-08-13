"use client";

import { useDashboardSummary } from "@/features/progress/hooks/use-dashboard-summary";
import { useHistory } from "@/features/progress/hooks/use-history";
import { useStudyStatistics } from "@/features/progress/hooks/use-study-statistics";
import { useSessionStore } from "@/store/session-store";

/**
 * Sin endpoint nuevo: arma el JSON con datos que la app ya cargo via React
 * Query (mismo query key que Dashboard/Estadisticas/Historial, sin llamada
 * de red extra) y dispara la descarga en el navegador.
 */
export function ExportProgressButton() {
  const user = useSessionStore((s) => s.user);
  const { data: summary } = useDashboardSummary();
  const { data: stats } = useStudyStatistics();
  const { data: history } = useHistory();

  const isReady = !!summary && !!stats && !!history;

  function handleExport() {
    const payload = {
      generated_at: new Date().toISOString(),
      profile: { full_name: user?.full_name, email: user?.email },
      summary,
      stats,
      history,
    };

    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "upmh-progreso.json";
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <button
      onClick={handleExport}
      disabled={!isReady}
      className="flex w-full items-center justify-between text-left disabled:opacity-50"
    >
      <div>
        <p className="text-sm font-medium text-foreground">Exportar progreso</p>
        <p className="text-sm text-foreground-muted">Descarga un reporte de tu progreso y resultados.</p>
      </div>
      <span aria-hidden="true" className="text-foreground-muted">
        ›
      </span>
    </button>
  );
}

import { useQuery } from "@tanstack/react-query";

import { fetchDashboardSummary } from "@/features/progress/api";

/**
 * Se usa tanto en el Header (para el badge de XP) como en la pantalla de
 * Dashboard. React Query deduplica automaticamente: si ambos estan
 * montados a la vez, es una sola llamada de red, no dos.
 */
export function useDashboardSummary() {
  return useQuery({
    queryKey: ["dashboard-summary"],
    queryFn: fetchDashboardSummary,
  });
}

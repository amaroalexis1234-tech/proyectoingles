import { useQuery } from "@tanstack/react-query";

import { fetchWeeklyEvolution } from "@/features/progress/api";

export function useWeeklyEvolution() {
  return useQuery({
    queryKey: ["weekly-evolution"],
    queryFn: fetchWeeklyEvolution,
  });
}

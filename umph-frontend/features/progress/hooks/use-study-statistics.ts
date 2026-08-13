import { useQuery } from "@tanstack/react-query";

import { fetchStudyStatistics } from "@/features/progress/api";

export function useStudyStatistics() {
  return useQuery({
    queryKey: ["study-statistics"],
    queryFn: fetchStudyStatistics,
  });
}

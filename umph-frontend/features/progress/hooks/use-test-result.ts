import { useQuery } from "@tanstack/react-query";

import { fetchTestResult } from "@/features/progress/api";

export function useTestResult(attemptId: string) {
  return useQuery({
    queryKey: ["test-result", attemptId],
    queryFn: () => fetchTestResult(attemptId),
    enabled: !!attemptId,
  });
}

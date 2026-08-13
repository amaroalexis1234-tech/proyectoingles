import { useQuery } from "@tanstack/react-query";

import { fetchInProgressAttempt } from "@/features/evaluations/api";

export function useInProgressAttempt() {
  return useQuery({
    queryKey: ["in-progress-attempt"],
    queryFn: fetchInProgressAttempt,
  });
}

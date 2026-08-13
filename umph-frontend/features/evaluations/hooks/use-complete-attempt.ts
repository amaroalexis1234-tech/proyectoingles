import { useMutation, useQueryClient } from "@tanstack/react-query";

import { completeAttempt } from "@/features/evaluations/api";

export function useCompleteAttempt() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: completeAttempt,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["dashboard-summary"] });
    },
  });
}

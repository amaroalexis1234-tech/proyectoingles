import { useMutation, useQueryClient } from "@tanstack/react-query";

import { activateStreakFreeze } from "@/features/progress/api";

export function useActivateStreakFreeze() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: activateStreakFreeze,
    onSuccess: (summary) => {
      queryClient.setQueryData(["dashboard-summary"], summary);
    },
  });
}

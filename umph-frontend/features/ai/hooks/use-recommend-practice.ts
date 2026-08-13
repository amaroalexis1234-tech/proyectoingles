import { useMutation } from "@tanstack/react-query";

import { recommendPractice } from "@/features/ai/api";

export function useRecommendPractice() {
  return useMutation({
    mutationFn: (attemptId: string) => recommendPractice(attemptId),
  });
}

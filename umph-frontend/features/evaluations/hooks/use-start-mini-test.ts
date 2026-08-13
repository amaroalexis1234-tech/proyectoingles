import { useMutation } from "@tanstack/react-query";

import { startMiniTest } from "@/features/evaluations/api";

export function useStartMiniTest() {
  return useMutation({
    mutationFn: ({ mode, numQuestions }: { mode: Parameters<typeof startMiniTest>[0]; numQuestions?: number }) =>
      startMiniTest(mode, numQuestions),
  });
}

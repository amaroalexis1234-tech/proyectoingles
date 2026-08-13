import { useMutation } from "@tanstack/react-query";

import { submitTestAnswer } from "@/features/evaluations/api";

export function useSubmitTestAnswer(attemptId: string) {
  return useMutation({
    mutationFn: ({ questionId, selectedAnswer }: { questionId: string; selectedAnswer: string }) =>
      submitTestAnswer(attemptId, questionId, selectedAnswer),
  });
}

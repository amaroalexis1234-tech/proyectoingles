import { useMutation } from "@tanstack/react-query";

import { explainQuestion } from "@/features/ai/api";

export function useExplainQuestion() {
  return useMutation({
    mutationFn: ({ questionId, studentAnswer }: { questionId: string; studentAnswer?: string }) =>
      explainQuestion(questionId, studentAnswer),
  });
}

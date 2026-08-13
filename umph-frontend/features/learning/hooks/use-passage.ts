import { useQuery } from "@tanstack/react-query";

import { fetchPassageWithQuestions } from "@/features/learning/api";

export function usePassage(passageId: string) {
  return useQuery({
    queryKey: ["passage", passageId],
    queryFn: () => fetchPassageWithQuestions(passageId),
    enabled: !!passageId,
  });
}

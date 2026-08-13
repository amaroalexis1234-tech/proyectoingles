import { useQuery } from "@tanstack/react-query";

import { fetchExercises, type Section } from "@/features/learning/api";

export function useExercises(section: Section, limit = 10) {
  return useQuery({
    queryKey: ["exercises", section, limit],
    queryFn: () => fetchExercises(section, limit),
  });
}

import { useQuery } from "@tanstack/react-query";

import { fetchReadingPassages } from "@/features/learning/api";

export function useReadingPassages() {
  return useQuery({ queryKey: ["reading-passages"], queryFn: fetchReadingPassages });
}

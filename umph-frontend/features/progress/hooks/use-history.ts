import { useQuery } from "@tanstack/react-query";

import { fetchHistory } from "@/features/progress/api";

export function useHistory() {
  return useQuery({ queryKey: ["progress-history"], queryFn: fetchHistory });
}

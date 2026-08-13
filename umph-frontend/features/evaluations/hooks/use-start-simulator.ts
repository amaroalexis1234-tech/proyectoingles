import { useMutation } from "@tanstack/react-query";

import { startSimulator } from "@/features/evaluations/api";

export function useStartSimulator() {
  return useMutation({ mutationFn: startSimulator });
}

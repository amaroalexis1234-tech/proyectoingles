import { useMutation, useQueryClient } from "@tanstack/react-query";

import { submitAttempt } from "@/features/learning/api";

export function useSubmitAttempt() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: submitAttempt,
    onSuccess: () => {
      // El XP/racha pudo haber cambiado: invalidamos el resumen del
      // dashboard para que el Header y el Dashboard se actualicen solos.
      queryClient.invalidateQueries({ queryKey: ["dashboard-summary"] });
    },
  });
}

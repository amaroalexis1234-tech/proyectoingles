import { useMutation } from "@tanstack/react-query";

import { registerRequest } from "@/features/auth/api";
import { useSessionStore } from "@/store/session-store";

export function useRegister() {
  const setSession = useSessionStore((s) => s.setSession);

  return useMutation({
    mutationFn: registerRequest,
    onSuccess: (data) => {
      setSession(data.user, data.access_token);
    },
  });
}

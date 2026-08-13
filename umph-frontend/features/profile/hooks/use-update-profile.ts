import { useMutation } from "@tanstack/react-query";

import { updateProfile } from "@/features/profile/api";
import { useSessionStore } from "@/store/session-store";

export function useUpdateProfile() {
  const setSession = useSessionStore((s) => s.setSession);
  const accessToken = useSessionStore((s) => s.accessToken);

  return useMutation({
    mutationFn: updateProfile,
    onSuccess: (user) => {
      if (accessToken) setSession(user, accessToken);
    },
  });
}

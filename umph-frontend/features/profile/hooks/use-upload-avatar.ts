import { useMutation } from "@tanstack/react-query";

import { uploadAvatar } from "@/features/profile/api";
import { useSessionStore } from "@/store/session-store";

export function useUploadAvatar() {
  const setSession = useSessionStore((s) => s.setSession);
  const accessToken = useSessionStore((s) => s.accessToken);

  return useMutation({
    mutationFn: uploadAvatar,
    onSuccess: (user) => {
      if (accessToken) setSession(user, accessToken);
    },
  });
}

import { useMutation } from "@tanstack/react-query";

import { changePassword } from "@/features/profile/api";

export function useChangePassword() {
  return useMutation({
    mutationFn: ({ currentPassword, newPassword }: { currentPassword: string; newPassword: string }) =>
      changePassword(currentPassword, newPassword),
  });
}

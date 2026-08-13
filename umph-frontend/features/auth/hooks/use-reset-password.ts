import { useMutation } from "@tanstack/react-query";

import { resetPasswordRequest } from "@/features/auth/api";

export function useResetPassword() {
  return useMutation({ mutationFn: resetPasswordRequest });
}

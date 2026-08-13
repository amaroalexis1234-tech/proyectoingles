"use client";

import { useMutation } from "@tanstack/react-query";

import { loginRequest } from "@/features/auth/api";
import { useSessionStore } from "@/store/session-store";

export function useLogin() {
  const setSession = useSessionStore((s) => s.setSession);

  return useMutation({
    mutationFn: loginRequest,
    onSuccess: (data) => {
      setSession(data.user, data.access_token);
    },
  });
}
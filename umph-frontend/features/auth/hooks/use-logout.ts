import { useRouter } from "next/navigation";

import { apiRequest } from "@/lib/api-client";
import { useSessionStore } from "@/store/session-store";

/**
 * Unica implementacion de logout -- antes duplicada en Header y en Profile.
 */
export function useLogout() {
  const router = useRouter();
  const clearSession = useSessionStore((s) => s.clearSession);

  return async function logout() {
    try {
      await apiRequest("/auth/logout", { method: "POST" });
    } finally {
      clearSession();
      router.push("/login");
    }
  };
}

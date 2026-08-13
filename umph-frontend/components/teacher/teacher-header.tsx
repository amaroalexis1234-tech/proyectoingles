"use client";

import { LogOut } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { useLogout } from "@/features/auth/hooks/use-logout";
import { useSessionStore } from "@/store/session-store";

export function TeacherHeader() {
  const user = useSessionStore((s) => s.user);
  const logout = useLogout();

  return (
    <header className="flex h-16 items-center justify-between border-b border-border bg-surface px-6">
      <div>
        <p className="text-sm text-foreground-muted">Hola, {user?.full_name?.split(" ")[0]}</p>
      </div>

      <div className="flex items-center gap-3">
        <Badge variant="secondary">Maestro</Badge>

        <button
          onClick={logout}
          className="flex h-9 w-9 items-center justify-center rounded text-foreground-muted transition-colors hover:bg-background hover:text-foreground"
          aria-label="Cerrar sesión"
        >
          <LogOut className="h-4 w-4" />
        </button>
      </div>
    </header>
  );
}

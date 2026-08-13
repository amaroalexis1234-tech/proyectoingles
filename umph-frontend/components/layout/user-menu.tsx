"use client";

import Link from "next/link";
import { ChevronDown, LogOut, Settings, User as UserIcon } from "lucide-react";

import { Avatar } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useLogout } from "@/features/auth/hooks/use-logout";
import { useSessionStore } from "@/store/session-store";

export function UserMenu() {
  const user = useSessionStore((s) => s.user);
  const logout = useLogout();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger className="flex items-center gap-2 rounded px-2 py-1.5 transition-colors hover:bg-background outline-none">
        <Avatar fullName={user?.full_name} avatarUrl={user?.avatar_url} size="sm" />
        <span className="hidden text-sm font-medium text-foreground sm:inline">
          {user?.full_name?.split(" ")[0]}
        </span>
        <ChevronDown className="hidden h-4 w-4 text-foreground-muted sm:inline" />
      </DropdownMenuTrigger>

      <DropdownMenuContent>
        <DropdownMenuItem asChild>
          <Link href="/profile">
            <UserIcon className="h-4 w-4" />
            Perfil
          </Link>
        </DropdownMenuItem>
        <DropdownMenuItem asChild>
          <Link href="/settings">
            <Settings className="h-4 w-4" />
            Configuración
          </Link>
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem danger onClick={logout}>
          <LogOut className="h-4 w-4" />
          Cerrar sesión
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

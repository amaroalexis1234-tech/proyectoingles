"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { cn } from "@/lib/utils";

const TABS = [
  { href: "/login", label: "Iniciar sesión" },
  { href: "/register", label: "Crear cuenta" },
];

export function AuthTabs() {
  const pathname = usePathname();

  return (
    <div className="flex rounded bg-background p-1">
      {TABS.map((tab) => {
        const isActive = pathname === tab.href;
        return (
          <Link
            key={tab.href}
            href={tab.href}
            className={cn(
              "flex-1 rounded px-4 py-2 text-center text-sm font-medium transition-colors",
              isActive
                ? "bg-surface text-foreground shadow-card"
                : "text-foreground-muted hover:text-foreground"
            )}
          >
            {tab.label}
          </Link>
        );
      })}
    </div>
  );
}

"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { NAV_ITEMS } from "@/components/layout/sidebar";
import { cn } from "@/lib/utils";

/**
 * Reemplaza al Sidebar en mobile (que se oculta con `hidden md:flex`).
 * Mismos NAV_ITEMS, nunca una lista de navegacion distinta -- solo
 * cambia la presentacion (barra inferior con scroll horizontal en vez
 * de columna lateral).
 */
export function MobileNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed inset-x-0 bottom-0 z-10 flex overflow-x-auto border-t border-border bg-surface md:hidden">
      {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
        const isActive = pathname === href || pathname.startsWith(`${href}/`);
        return (
          <Link
            key={href}
            href={href}
            className={cn(
              "flex min-w-[4.5rem] flex-1 flex-col items-center gap-1 px-2 py-2.5 text-[11px] font-medium",
              isActive ? "text-primary" : "text-foreground-muted"
            )}
          >
            <Icon className="h-5 w-5" />
            <span className="whitespace-nowrap">{label}</span>
          </Link>
        );
      })}
    </nav>
  );
}

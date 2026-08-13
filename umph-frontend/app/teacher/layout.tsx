"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { TeacherHeader } from "@/components/teacher/teacher-header";
import { TeacherSidebar } from "@/components/teacher/teacher-sidebar";
import { useSessionStore } from "@/store/session-store";

/**
 * Guard de cliente: redirige si no es maestro. La proteccion real vive en
 * el backend (CurrentTeacherDep) -- esto solo evita mostrar la pantalla
 * un instante antes de que cualquier fetch falle con 403.
 */
export default function TeacherLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const user = useSessionStore((s) => s.user);

  useEffect(() => {
    if (user && user.role !== "teacher") {
      router.replace("/dashboard");
    }
  }, [user, router]);

  if (user && user.role !== "teacher") {
    return null;
  }

  return (
    <div className="flex min-h-screen bg-background">
      <TeacherSidebar />
      <div className="flex flex-1 flex-col">
        <TeacherHeader />
        <main className="flex-1">{children}</main>
      </div>
    </div>
  );
}

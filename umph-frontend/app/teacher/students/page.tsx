"use client";

import Link from "next/link";
import { Flame, Sparkles } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import { useStudents } from "@/features/teacher/hooks/use-students";

export default function TeacherStudentsPage() {
  const { data: students, isLoading } = useStudents();

  if (isLoading || !students) {
    return (
      <div className="p-6">
        <div className="h-6 w-40 animate-pulse rounded bg-surface" />
      </div>
    );
  }

  return (
    <div className="animate-fade-in space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Alumnos</h1>
        <p className="text-sm text-foreground-muted">Revisa el avance de cada alumno.</p>
      </div>

      {students.length === 0 ? (
        <Card>
          <CardContent className="pt-2 text-sm text-foreground-muted">Todavía no hay alumnos registrados.</CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {students.map((student) => (
            <Link key={student.id} href={`/teacher/students/${student.id}`}>
              <Card className="transition-colors hover:border-primary">
                <CardContent className="flex items-center justify-between pt-2">
                  <div>
                    <p className="text-sm font-medium text-foreground">{student.full_name}</p>
                    <p className="text-xs text-foreground-muted">{student.email}</p>
                  </div>
                  <div className="flex items-center gap-4 text-sm">
                    <span className="flex items-center gap-1.5 text-foreground-muted">
                      <Sparkles className="h-4 w-4" />
                      {student.current_xp} XP
                    </span>
                    <span className="flex items-center gap-1.5 text-foreground-muted">
                      <Flame className="h-4 w-4" />
                      {student.streak_days} {student.streak_days === 1 ? "día" : "días"}
                    </span>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

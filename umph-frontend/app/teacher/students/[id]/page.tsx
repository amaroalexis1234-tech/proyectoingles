"use client";

import { useParams } from "next/navigation";

import { LevelBadge } from "@/components/layout/level-badge";
import { Card } from "@/components/ui/card";
import { AccuracyDonut } from "@/features/progress/components/accuracy-donut";
import { AttemptHistoryList } from "@/features/progress/components/attempt-history-list";
import { StudyStatisticsGrid } from "@/features/progress/components/study-statistics-grid";
import { useStudentDetail } from "@/features/teacher/hooks/use-student-detail";
import { useStudents } from "@/features/teacher/hooks/use-students";

export default function TeacherStudentDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: students } = useStudents();
  const { summary, stats, history } = useStudentDetail(id);

  const student = students?.find((s) => s.id === id);

  if (summary.isLoading || stats.isLoading || !summary.data || !stats.data) {
    return (
      <div className="p-6">
        <div className="h-6 w-40 animate-pulse rounded bg-surface" />
      </div>
    );
  }

  return (
    <div className="animate-fade-in mx-auto max-w-3xl space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">
          {student?.full_name ?? "Alumno"}
        </h1>
        <p className="text-sm text-foreground-muted">{student?.email}</p>
      </div>

      <div className="max-w-xs">
        <LevelBadge xpLevel={summary.data.xp_level} level={summary.data.level} variant="card" />
      </div>

      <Card>
        <AccuracyDonut
          correct={stats.data.correct_count}
          incorrect={stats.data.incorrect_count}
          unanswered={stats.data.unanswered_count}
        />
      </Card>

      <StudyStatisticsGrid stats={stats.data} />

      <div>
        <h2 className="mb-3 text-base font-semibold text-foreground">Historial de evaluaciones</h2>
        {history.isLoading || !history.data ? (
          <div className="h-24 animate-pulse rounded bg-surface" />
        ) : (
          <AttemptHistoryList attempts={history.data} linkToResults={false} />
        )}
      </div>
    </div>
  );
}

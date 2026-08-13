import { useQuery } from "@tanstack/react-query";

import { fetchStudentHistory, fetchStudentStats, fetchStudentSummary } from "@/features/teacher/api";

export function useStudentDetail(studentId: string) {
  const summary = useQuery({
    queryKey: ["teacher-student-summary", studentId],
    queryFn: () => fetchStudentSummary(studentId),
    enabled: !!studentId,
  });
  const stats = useQuery({
    queryKey: ["teacher-student-stats", studentId],
    queryFn: () => fetchStudentStats(studentId),
    enabled: !!studentId,
  });
  const history = useQuery({
    queryKey: ["teacher-student-history", studentId],
    queryFn: () => fetchStudentHistory(studentId),
    enabled: !!studentId,
  });

  return { summary, stats, history };
}

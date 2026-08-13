import { useQuery } from "@tanstack/react-query";

import { fetchStudents } from "@/features/teacher/api";

export function useStudents() {
  return useQuery({ queryKey: ["teacher-students"], queryFn: fetchStudents });
}

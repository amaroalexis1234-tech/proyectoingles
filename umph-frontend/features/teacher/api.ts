import { apiRequest } from "@/lib/api-client";
import type { DashboardSummary, StudyStatistics, TestAttemptSummary } from "@/features/progress/api";

export interface StudentSummary {
  id: string;
  full_name: string;
  email: string;
  current_xp: number;
  streak_days: number;
}

export function fetchStudents() {
  return apiRequest<StudentSummary[]>("/teacher/students");
}

export function fetchStudentSummary(studentId: string) {
  return apiRequest<DashboardSummary>(`/teacher/students/${studentId}/summary`);
}

export function fetchStudentStats(studentId: string) {
  return apiRequest<StudyStatistics>(`/teacher/students/${studentId}/stats`);
}

export function fetchStudentHistory(studentId: string) {
  return apiRequest<TestAttemptSummary[]>(`/teacher/students/${studentId}/history`);
}

// --- Banco de preguntas ---

export type Section = "structure" | "written_expression" | "reading" | "vocabulary";
export type QuestionType = "sentence_completion" | "error_identification" | "multiple_choice" | "vocabulary_choice";

export interface QuestionRead {
  id: string;
  section: Section;
  question_type: QuestionType;
  prompt: string;
  options: Record<string, string>;
  correct_answer: string;
  explanation: string | null;
  passage_id: string | null;
  verified: boolean;
  source: string;
}

export interface QuestionCreate {
  section: Section;
  question_type: QuestionType;
  prompt: string;
  options: Record<string, string>;
  correct_answer: string;
  explanation?: string;
  passage_id?: string;
}

export interface PassageRead {
  id: string;
  title: string | null;
  text: string;
  source: string;
}

export interface PassageCreate {
  title?: string;
  text: string;
  source: string;
}

export function fetchQuestions(section?: Section) {
  const query = section ? `?section=${section}` : "";
  return apiRequest<QuestionRead[]>(`/question-bank/questions${query}`);
}

export function createQuestion(data: QuestionCreate) {
  return apiRequest<QuestionRead>("/question-bank/questions", { method: "POST", body: data });
}

export function deleteQuestion(questionId: string) {
  return apiRequest<void>(`/question-bank/questions/${questionId}`, { method: "DELETE" });
}

export function fetchPassages() {
  return apiRequest<PassageRead[]>("/question-bank/passages");
}

export function createPassage(data: PassageCreate) {
  return apiRequest<PassageRead>("/question-bank/passages", { method: "POST", body: data });
}

export interface QuestionImportError {
  row: number;
  message: string;
}

export interface QuestionImportResult {
  created: number;
  errors: QuestionImportError[];
}

export function importQuestionsCsv(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  return apiRequest<QuestionImportResult>("/question-bank/questions/import", { method: "POST", body: formData });
}

export interface QuestionAnalytics {
  question_id: string;
  section: Section;
  prompt: string;
  attempts_count: number;
  correct_count: number;
  accuracy_percent: number;
}

export interface QuestionAnalyticsResponse {
  questions: QuestionAnalytics[];
  untried_count: number;
}

export function fetchQuestionAnalytics() {
  return apiRequest<QuestionAnalyticsResponse>("/teacher/questions/analytics");
}

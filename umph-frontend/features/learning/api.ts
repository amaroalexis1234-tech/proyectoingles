import { apiRequest } from "@/lib/api-client";

export type Section = "structure" | "written_expression" | "reading" | "vocabulary";

export interface QuestionPublic {
  id: string;
  section: Section;
  question_type: string;
  prompt: string;
  options: Record<string, string>;
  passage_id: string | null;
}

export interface PassageSummary {
  id: string;
  title: string | null;
}

export interface PassageWithQuestions {
  passage_id: string;
  title: string | null;
  text: string;
  questions: QuestionPublic[];
}

export interface SubmitAttemptPayload {
  question_id: string;
  selected_answer: string;
  time_spent_seconds?: number;
}

export interface SubmitAttemptResponse {
  is_correct: boolean;
  correct_answer: string;
  explanation: string | null;
  xp_awarded: number;
}

export function fetchExercises(section: Section, limit = 10) {
  return apiRequest<QuestionPublic[]>(`/learning/exercises?section=${section}&limit=${limit}`);
}

export function fetchReadingPassages() {
  return apiRequest<PassageSummary[]>("/learning/reading/passages");
}

export function fetchPassageWithQuestions(passageId: string) {
  return apiRequest<PassageWithQuestions>(`/learning/reading/passages/${passageId}`);
}

export function submitAttempt(payload: SubmitAttemptPayload) {
  return apiRequest<SubmitAttemptResponse>("/learning/attempts", {
    method: "POST",
    body: payload,
  });
}

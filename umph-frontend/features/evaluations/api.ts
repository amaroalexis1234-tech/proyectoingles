import { apiRequest } from "@/lib/api-client";
import type { QuestionPublic } from "@/features/learning/api";

export type MiniTestMode = "grammar" | "reading" | "mixed" | "official";
export type TestType = "mini_test" | "simulator";

export interface PassageContext {
  id: string;
  title: string | null;
  text: string;
}

export interface TestAttemptItemPublic {
  order_index: number;
  question: QuestionPublic;
  answered: boolean;
  selected_answer: string | null;
}

export interface TestAttemptStarted {
  test_attempt_id: string;
  test_type: TestType;
  mini_test_mode: MiniTestMode | null;
  total_questions: number;
  time_limit_seconds: number | null;
  started_at: string;
  items: TestAttemptItemPublic[];
  passages: PassageContext[];
}

export interface SubmitTestAnswerResponse {
  recorded: boolean;
  is_correct: boolean | null;
  correct_answer: string | null;
  explanation: string | null;
}

export interface SectionScore {
  correct: number;
  total: number;
}

export interface TestResult {
  test_attempt_id: string;
  total_questions: number;
  correct_count: number;
  accuracy: number;
  section_scores: Record<string, SectionScore>;
  xp_awarded: number;
  started_at: string;
  completed_at: string;
}

export function startMiniTest(mode: MiniTestMode, num_questions = 20) {
  return apiRequest<TestAttemptStarted>("/evaluations/mini-tests", {
    method: "POST",
    body: { mode, num_questions },
  });
}

export function startSimulator() {
  return apiRequest<TestAttemptStarted>("/evaluations/simulator", { method: "POST" });
}

export function fetchAttempt(attemptId: string) {
  return apiRequest<TestAttemptStarted>(`/evaluations/attempts/${attemptId}`);
}

export function submitTestAnswer(attemptId: string, questionId: string, selectedAnswer: string) {
  return apiRequest<SubmitTestAnswerResponse>(`/evaluations/attempts/${attemptId}/answers`, {
    method: "POST",
    body: { question_id: questionId, selected_answer: selectedAnswer },
  });
}

export function completeAttempt(attemptId: string) {
  return apiRequest<TestResult>(`/evaluations/attempts/${attemptId}/complete`, { method: "POST" });
}

export interface InProgressAttempt {
  id: string;
  test_type: TestType;
  mini_test_mode: MiniTestMode | null;
  total_questions: number;
  answered_count: number;
  started_at: string;
}

export function fetchInProgressAttempt() {
  return apiRequest<InProgressAttempt | null>("/evaluations/attempts/in-progress");
}

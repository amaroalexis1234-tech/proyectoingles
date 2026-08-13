import { apiRequest } from "@/lib/api-client";

export interface VocabularyTerm {
  term: string;
  translation: string;
}

export interface ExplainResponse {
  explanation: string;
  evidence: string | null;
  vocabulary_terms: VocabularyTerm[] | null;
  grammar_rule: string | null;
  translation: string | null;
  source: "ai" | "fallback";
}

export function explainQuestion(questionId: string, studentAnswer?: string) {
  return apiRequest<ExplainResponse>("/ai/explain", {
    method: "POST",
    body: { question_id: questionId, student_answer: studentAnswer },
  });
}

export interface RecommendationResponse {
  recommendation: string;
  source: "ai" | "fallback";
}

export function recommendPractice(attemptId: string) {
  return apiRequest<RecommendationResponse>("/ai/recommend-practice", {
    method: "POST",
    body: { attempt_id: attemptId },
  });
}

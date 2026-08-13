import { apiRequest } from "@/lib/api-client";
import type { TestResult } from "@/features/evaluations/api";

export interface WeakSkill {
  skill_number: number;
  section: string;
  accuracy: number;
}

export interface QuickPracticeSuggestion {
  section: string;
  reason: string;
}

export interface LevelEstimate {
  estimated_score: number;
  cefr_band: string;
  band_progress_percent: number;
  based_on_attempts: number;
}

export interface XpLevel {
  level: number;
  current_xp_in_level: number;
  xp_for_next_level: number;
}

export interface DailyGoal {
  target_count: number;
  completed_count: number;
  completed: boolean;
}

export interface StudyStatistics {
  questions_answered: number;
  accuracy_percent: number | null;
  study_time_seconds: number;
  completed_simulators: number;
  completed_mini_tests: number;
  day_streak: number;
  correct_count: number;
  incorrect_count: number;
  unanswered_count: number;
}

export interface WeeklyEvolutionDay {
  day_label: string;
  accuracy_percent: number | null;
}

export interface DashboardSummary {
  current_xp: number;
  streak_days: number;
  weak_skills: WeakSkill[];
  quick_practice: QuickPracticeSuggestion[];
  has_enough_data_for_recommendations: boolean;
  xp_level: XpLevel;
  level: LevelEstimate | null;
  has_enough_data_for_level: boolean;
  daily_goal: DailyGoal;
  streak_freeze_available: boolean;
}

export interface TestAttemptSummary {
  id: string;
  test_type: "mini_test" | "simulator";
  mini_test_mode: string | null;
  completed_at: string;
  total_questions: number;
  correct_count: number;
  accuracy: number;
}

export function fetchHistory() {
  return apiRequest<TestAttemptSummary[]>("/progress/history");
}

export function fetchDashboardSummary() {
  return apiRequest<DashboardSummary>("/progress/dashboard");
}

export function activateStreakFreeze() {
  return apiRequest<DashboardSummary>("/progress/streak-freeze", { method: "POST" });
}

export function fetchStudyStatistics() {
  return apiRequest<StudyStatistics>("/progress/stats");
}

export function fetchWeeklyEvolution() {
  return apiRequest<WeeklyEvolutionDay[]>("/progress/weekly-evolution");
}

export function fetchTestResult(attemptId: string) {
  return apiRequest<TestResult>(`/progress/results/${attemptId}`);
}

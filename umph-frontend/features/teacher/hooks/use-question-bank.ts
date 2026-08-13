import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  createPassage,
  createQuestion,
  deleteQuestion,
  fetchPassages,
  fetchQuestionAnalytics,
  fetchQuestions,
  importQuestionsCsv,
  type PassageCreate,
  type QuestionCreate,
  type Section,
} from "@/features/teacher/api";

export function useQuestions(section?: Section) {
  return useQuery({
    queryKey: ["question-bank-questions", section ?? "all"],
    queryFn: () => fetchQuestions(section),
  });
}

export function usePassages() {
  return useQuery({ queryKey: ["question-bank-passages"], queryFn: fetchPassages });
}

export function useCreateQuestion() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: QuestionCreate) => createQuestion(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["question-bank-questions"] });
    },
  });
}

export function useCreatePassage() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: PassageCreate) => createPassage(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["question-bank-passages"] });
    },
  });
}

export function useDeleteQuestion() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (questionId: string) => deleteQuestion(questionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["question-bank-questions"] });
    },
  });
}

export function useQuestionAnalytics() {
  return useQuery({ queryKey: ["question-bank-analytics"], queryFn: fetchQuestionAnalytics });
}

export function useImportQuestionsCsv() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (file: File) => importQuestionsCsv(file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["question-bank-questions"] });
    },
  });
}

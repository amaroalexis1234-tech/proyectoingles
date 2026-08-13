"use client";

import { ExercisePractice } from "@/features/learning/components/exercise-practice";

export default function VocabularyPracticePage() {
  return (
    <ExercisePractice
      section="vocabulary"
      title="Vocabulary"
      description="Elige el sinónimo más cercano a la palabra subrayada."
      renderPromptAsHtml
    />
  );
}

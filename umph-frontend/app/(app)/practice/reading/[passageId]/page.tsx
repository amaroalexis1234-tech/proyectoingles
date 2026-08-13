"use client";

import { useParams } from "next/navigation";

import { ReadingPractice } from "@/features/learning/components/reading-practice";

export default function ReadingPassagePage() {
  const params = useParams<{ passageId: string }>();
  return <ReadingPractice passageId={params.passageId} />;
}

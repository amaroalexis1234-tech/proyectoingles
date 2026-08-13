import Link from "next/link";
import { Sparkles } from "lucide-react";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { QuickPracticeSuggestion } from "@/features/progress/api";

const SECTION_ROUTES: Record<string, string> = {
  structure: "/practice/structure",
  written_expression: "/practice/written-expression",
  reading: "/practice/reading",
  vocabulary: "/practice/vocabulary",
};

const SECTION_LABELS: Record<string, string> = {
  structure: "Structure",
  written_expression: "Written Expression",
  reading: "Reading",
  vocabulary: "Vocabulary",
};

/**
 * Renombrado desde quick-practice-card.tsx: el mockup usa "Quick Practice"
 * para una grilla ESTATICA distinta (ver quick-practice-shortcuts.tsx) --
 * esta es la sugerencia DINAMICA basada en secciones debiles, mismo
 * contrato de datos y estado vacio honesto de siempre.
 */
export function RecommendedPracticeCard({ suggestions }: { suggestions: QuickPracticeSuggestion[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <Sparkles className="h-4 w-4 text-foreground-muted" />
          Recomendado para ti
        </CardTitle>
        <CardDescription>Sugerido según tu actividad reciente.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-2">
        {suggestions.map((suggestion) => (
          <Link
            key={suggestion.section}
            href={SECTION_ROUTES[suggestion.section] ?? "/dashboard"}
            className="block rounded border border-border px-3 py-2.5 text-sm transition-colors hover:border-primary hover:bg-primary/5"
          >
            <p className="font-medium text-foreground">{SECTION_LABELS[suggestion.section] ?? suggestion.section}</p>
            <p className="text-foreground-muted">{suggestion.reason}</p>
          </Link>
        ))}
      </CardContent>
    </Card>
  );
}

import { Target } from "lucide-react";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import type { WeakSkill } from "@/features/progress/api";

const SECTION_LABELS: Record<string, string> = {
  structure: "Structure",
  written_expression: "Written Expression",
  reading: "Reading",
  vocabulary: "Vocabulary",
};

// No se muestran nombres de skill (ej. "Main Idea") porque no hay en este
// proyecto el material fuente que confirme que representa cada numero --
// inventar arriesga poner informacion academica incorrecta. Decision
// confirmada explicitamente, ver plan de Modulo 2.
export function WeakSkillsCard({ skills }: { skills: WeakSkill[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <Target className="h-4 w-4 text-foreground-muted" />
          Weak Skills
        </CardTitle>
        <CardDescription>Basado en tus intentos recientes.</CardDescription>
      </CardHeader>
      <CardContent>
        {skills.length === 0 ? (
          <p className="text-sm text-foreground-muted">
            Vas bien — ningún skill está claramente por debajo del resto todavía.
          </p>
        ) : (
          <ul className="space-y-3">
            {skills.map((skill) => (
              <li key={`${skill.section}-${skill.skill_number}`}>
                <div className="mb-1 flex items-center justify-between text-sm">
                  <span className="text-foreground">
                    {SECTION_LABELS[skill.section] ?? skill.section} — Skill {skill.skill_number}
                  </span>
                  <span className="text-error">{skill.accuracy}%</span>
                </div>
                <Progress value={skill.accuracy} />
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}

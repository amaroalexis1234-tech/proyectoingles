import Link from "next/link";
import { ClipboardCheck, Timer } from "lucide-react";

import { Card, CardContent, CardDescription, CardTitle } from "@/components/ui/card";

export default function EvaluationsPage() {
  return (
    <div className="animate-fade-in space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Evaluaciones</h1>
        <p className="text-sm text-foreground-muted">Pon a prueba lo que has practicado.</p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <Link href="/evaluations/mini-test">
          <Card className="h-full transition-colors hover:border-primary">
            <CardContent className="space-y-2 pt-2">
              <ClipboardCheck className="h-6 w-6 text-primary" />
              <CardTitle className="text-base">Mini Test</CardTitle>
              <CardDescription>
                Practica corta y con retroalimentación inmediata. Elige entre Grammar, Reading, Mixed u Official.
              </CardDescription>
            </CardContent>
          </Card>
        </Link>

        <Link href="/evaluations/simulator">
          <Card className="h-full transition-colors hover:border-primary">
            <CardContent className="space-y-2 pt-2">
              <Timer className="h-6 w-6 text-primary" />
              <CardTitle className="text-base">Simulador Oficial</CardTitle>
              <CardDescription>
                Réplica exacta del examen: Structure (15) + Written Expression (25) en 25 min, Reading (5 pasajes) en 55 min. Sin ayudas.
              </CardDescription>
            </CardContent>
          </Card>
        </Link>
      </div>
    </div>
  );
}

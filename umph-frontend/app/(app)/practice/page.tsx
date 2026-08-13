import Link from "next/link";
import { BookOpen, ClipboardCheck, Monitor, PenSquare, SpellCheck } from "lucide-react";

import { Card } from "@/components/ui/card";

const OPTIONS = [
  { href: "/practice/reading", label: "Reading", description: "Comprende textos reales y responde preguntas.", icon: BookOpen, color: "text-primary bg-primary/10" },
  { href: "/practice/structure", label: "Structure", description: "Mejora tu gramática en contexto.", icon: PenSquare, color: "text-accent-green bg-accent-green/10" },
  { href: "/practice/written-expression", label: "Written Expression", description: "Desarrolla tu escritura con precisión.", icon: SpellCheck, color: "text-accent-purple bg-accent-purple/10" },
  { href: "/practice/vocabulary", label: "Vocabulary", description: "Amplía tu vocabulario clave para el examen.", icon: SpellCheck, color: "text-accent-orange bg-accent-orange/10" },
  { href: "/evaluations/mini-test", label: "Mini Test", description: "Practica con tests cortos y enfocados.", icon: ClipboardCheck, color: "text-primary bg-primary/10" },
  { href: "/evaluations/simulator", label: "Simulador", description: "Presenta un examen completo como el oficial.", icon: Monitor, color: "text-accent-green bg-accent-green/10" },
];

export default function PracticeHubPage() {
  return (
    <div className="animate-fade-in space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">¿Qué quieres practicar hoy?</h1>
        <p className="text-sm text-foreground-muted">Elige la habilidad que deseas fortalecer.</p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {OPTIONS.map(({ href, label, description, icon: Icon, color }) => (
          <Link key={href} href={href}>
            <Card className="h-full transition-colors hover:border-primary">
              <div className={`mb-4 flex h-11 w-11 items-center justify-center rounded ${color}`}>
                <Icon className="h-5 w-5" />
              </div>
              <p className="font-semibold text-foreground">{label}</p>
              <p className="text-sm text-foreground-muted">{description}</p>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}

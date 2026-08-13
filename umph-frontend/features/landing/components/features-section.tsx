import { BookOpen, PenSquare, Sparkles, SpellCheck } from "lucide-react";

import { FeatureCard } from "./feature-card";

const FEATURES = [
  {
    icon: BookOpen,
    title: "Reading",
    description: "Mejora tu comprensión lectora con textos reales y preguntas tipo examen.",
    color: "blue" as const,
  },
  {
    icon: PenSquare,
    title: "Grammar",
    description: "Practica gramática en contexto con ejercicios interactivos.",
    color: "green" as const,
  },
  {
    icon: SpellCheck,
    title: "Written Expression",
    description: "Desarrolla tu escritura con ejercicios similares al examen oficial.",
    color: "purple" as const,
  },
  {
    icon: Sparkles,
    title: "Feedback con IA",
    description: "Obtén explicaciones claras y personalizadas al instante.",
    color: "orange" as const,
  },
];

export function FeaturesSection() {
  return (
    <section id="caracteristicas" className="bg-surface py-16 sm:py-24">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="mx-auto max-w-xl space-y-2 text-center">
          <p className="text-sm font-semibold uppercase tracking-wide text-primary">
            Todo lo que necesitas
          </p>
          <h2 className="text-3xl font-semibold tracking-tight text-foreground">
            Características principales
          </h2>
        </div>

        <div className="mt-10 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {FEATURES.map((feature) => (
            <FeatureCard key={feature.title} {...feature} />
          ))}
        </div>
      </div>
    </section>
  );
}

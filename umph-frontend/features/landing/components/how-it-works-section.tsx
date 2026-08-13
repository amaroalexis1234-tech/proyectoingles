import { BarChart3, Target, Trophy } from "lucide-react";

const STEPS = [
  { number: 1, icon: Target, title: "Practica", description: "Elige el tema o examen que quieres practicar." },
  { number: 2, icon: BarChart3, title: "Aprende", description: "Recibe retroalimentación inteligente y mejora." },
  { number: 3, icon: Trophy, title: "Aprueba", description: "Gana confianza y alcanza tus objetivos." },
];

export function HowItWorksSection() {
  return (
    <section id="como-funciona" className="mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-24">
      <h2 className="text-center text-3xl font-semibold tracking-tight text-foreground">
        ¿Cómo funciona?
      </h2>

      <div className="mt-12 flex flex-col items-center gap-10 sm:flex-row sm:items-start sm:justify-center sm:gap-4">
        {STEPS.map((step, index) => (
          <div key={step.number} className="flex items-center sm:contents">
            <div className="flex w-48 flex-col items-center gap-3 text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary text-primary-foreground">
                <step.icon className="h-6 w-6" />
              </div>
              <h3 className="font-semibold text-foreground">{step.title}</h3>
              <p className="text-sm text-foreground-muted">{step.description}</p>
            </div>

            {index < STEPS.length - 1 && (
              <div className="hidden h-px w-12 shrink-0 bg-border sm:mt-8 sm:block" />
            )}
          </div>
        ))}
      </div>
    </section>
  );
}

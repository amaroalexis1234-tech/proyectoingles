import Link from "next/link";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

import { HeroIllustration } from "./hero-illustration";

export function HeroSection() {
  return (
    <section id="inicio" className="mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-24">
      <div className="grid items-center gap-10 lg:grid-cols-2 lg:gap-16">
        <div className="space-y-6">
          <Badge>Prepárate para el éxito</Badge>

          <h1 className="text-4xl font-semibold tracking-tight text-foreground sm:text-5xl">
            Domina el examen de inglés de la UPMH
          </h1>

          <p className="max-w-lg text-base text-foreground-muted sm:text-lg">
            Practica con exámenes similares, recibe retroalimentación inteligente y mejora tus
            habilidades paso a paso.
          </p>

          <div className="flex flex-wrap gap-3">
            <Button asChild size="lg">
              <Link href="/register">
                Comenzar ahora
                <span aria-hidden="true">→</span>
              </Link>
            </Button>
            <Button asChild variant="secondary" size="lg">
              <a href="#caracteristicas">Ver más</a>
            </Button>
          </div>
        </div>

        <HeroIllustration />
      </div>
    </section>
  );
}

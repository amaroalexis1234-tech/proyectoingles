import { BadgeCheck, BookOpen, Laptop, PenLine } from "lucide-react";

/**
 * Composicion placeholder (sin asset externo) hasta que exista una
 * ilustracion real -- aislada en su propio archivo para que reemplazarla
 * despues sea un cambio de un solo componente.
 */
export function HeroIllustration() {
  return (
    <div className="relative flex h-72 w-full items-center justify-center sm:h-96">
      <div className="absolute h-56 w-56 rounded-full bg-primary/10 sm:h-72 sm:w-72" />

      <div className="relative flex h-28 w-40 items-center justify-center rounded bg-surface shadow-card sm:h-36 sm:w-52">
        <Laptop className="h-12 w-12 text-primary sm:h-16 sm:w-16" strokeWidth={1.5} />
      </div>

      <div className="absolute left-4 top-6 flex h-12 w-12 items-center justify-center rounded bg-primary text-primary-foreground shadow-card sm:left-8 sm:top-10 sm:h-14 sm:w-14">
        <PenLine className="h-5 w-5 sm:h-6 sm:w-6" />
      </div>

      <div className="absolute right-6 top-4 flex h-11 w-11 items-center justify-center rounded bg-accent-orange text-white shadow-card sm:right-10 sm:top-8 sm:h-12 sm:w-12">
        <BookOpen className="h-5 w-5" />
      </div>

      <div className="absolute bottom-6 right-8 flex h-11 w-11 items-center justify-center rounded bg-success text-white shadow-card sm:bottom-10 sm:right-12 sm:h-12 sm:w-12">
        <BadgeCheck className="h-5 w-5" />
      </div>
    </div>
  );
}

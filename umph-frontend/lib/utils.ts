import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Combina clases condicionalmente y resuelve conflictos de Tailwind
 * (ej. "p-2 p-4" -> se queda solo con "p-4"). Se usa en todos los
 * componentes ui/ para permitir className como prop sin romper estilos base.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

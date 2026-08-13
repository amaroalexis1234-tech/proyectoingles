import { GraduationCap } from "lucide-react";

/**
 * Composicion placeholder para el panel izquierdo de auth -- vive siempre
 * sobre bg-auth-aside, por eso usa blancos/opacidades fijas en vez de
 * tokens de texto de pagina (el panel no se "apaga" con el contenido).
 */
export function AuthIllustration() {
  return (
    <div className="relative flex h-48 w-full items-center justify-center">
      <div className="absolute h-40 w-40 rounded-full bg-white/10" />
      <div className="relative flex h-24 w-24 items-center justify-center rounded-full bg-white/15">
        <GraduationCap className="h-11 w-11 text-white" strokeWidth={1.5} />
      </div>
    </div>
  );
}

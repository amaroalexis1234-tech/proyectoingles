import { AuthAsidePanel } from "@/features/auth/components/auth-aside-panel";

/**
 * Shell compartido de las 4 rutas de auth (login/registro/forgot/reset):
 * panel izquierdo de marca (oculto en mobile) + columna derecha centrada
 * donde cada pantalla pone su propio contenido.
 */
export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid min-h-screen bg-background lg:grid-cols-[2fr_3fr]">
      <AuthAsidePanel />

      <div className="flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-md">{children}</div>
      </div>
    </div>
  );
}

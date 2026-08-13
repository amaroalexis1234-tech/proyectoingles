import Link from "next/link";

import { AuthDivider } from "@/features/auth/components/auth-divider";
import { AuthTabs } from "@/features/auth/components/auth-tabs";
import { RegisterForm } from "@/features/auth/components/register-form";
import { OAuthButtons } from "@/features/auth/components/oauth-buttons";

export default function RegisterPage() {
  return (
    <div className="animate-fade-in space-y-6">
      <AuthTabs />

      <div className="space-y-1">
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Crea tu cuenta</h1>
        <p className="text-sm text-foreground-muted">
          Empieza a practicar para tu examen TOEFL ITP.
        </p>
      </div>

      <RegisterForm />

      <AuthDivider />
      <OAuthButtons />

      <p className="text-center text-sm text-foreground-muted">
        ¿Ya tienes cuenta?{" "}
        <Link href="/login" className="font-medium text-primary hover:underline">
          Inicia sesión
        </Link>
      </p>
    </div>
  );
}

import Link from "next/link";

import { AuthDivider } from "@/features/auth/components/auth-divider";
import { AuthTabs } from "@/features/auth/components/auth-tabs";
import { LoginForm } from "@/features/auth/components/login-form";
import { OAuthButtons } from "@/features/auth/components/oauth-buttons";

export default function LoginPage() {
  return (
    <div className="animate-fade-in space-y-6">
      <AuthTabs />

      <div className="space-y-1">
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">
          ¡Bienvenido de nuevo!
        </h1>
        <p className="text-sm text-foreground-muted">Ingresa tus datos para continuar</p>
      </div>

      <LoginForm />

      <AuthDivider />
      <OAuthButtons />

      <p className="text-center text-sm text-foreground-muted">
        ¿No tienes cuenta?{" "}
        <Link href="/register" className="font-medium text-primary hover:underline">
          Regístrate
        </Link>
      </p>
    </div>
  );
}

import { ForgotPasswordForm } from "@/features/auth/components/forgot-password-form";

export default function ForgotPasswordPage() {
  return (
    <div className="animate-fade-in space-y-6">
      <div className="space-y-1">
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">
          Recupera tu contraseña
        </h1>
        <p className="text-sm text-foreground-muted">Te enviaremos un enlace para restablecerla.</p>
      </div>

      <ForgotPasswordForm />
    </div>
  );
}

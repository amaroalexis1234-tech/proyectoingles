import { Suspense } from "react";

import { ResetPasswordForm } from "@/features/auth/components/reset-password-form";

export default function ResetPasswordPage() {
  return (
    <div className="animate-fade-in space-y-6">
      <div className="space-y-1">
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">
          Restablecer contraseña
        </h1>
        <p className="text-sm text-foreground-muted">Elige una nueva contraseña para tu cuenta.</p>
      </div>

      {/* useSearchParams requiere Suspense en build estatico (App Router) */}
      <Suspense fallback={null}>
        <ResetPasswordForm />
      </Suspense>
    </div>
  );
}

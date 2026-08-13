"use client";

import { useState, type FormEvent } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useResetPassword } from "@/features/auth/hooks/use-reset-password";
import { ApiError } from "@/lib/api-client";

export function ResetPasswordForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token");

  const resetPassword = useResetPassword();
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [formError, setFormError] = useState<string | null>(null);

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setFormError(null);

    if (newPassword !== confirmPassword) {
      setFormError("Las contraseñas no coinciden.");
      return;
    }
    if (!token) {
      setFormError("El enlace no es válido: falta el token de recuperación.");
      return;
    }

    resetPassword.mutate(
      { token, new_password: newPassword },
      {
        onError: (error) => {
          setFormError(
            error instanceof ApiError
              ? "El enlace expiró o ya fue usado. Solicita uno nuevo."
              : "No se pudo restablecer la contraseña. Intenta de nuevo."
          );
        },
      }
    );
  }

  if (!token) {
    return (
      <div className="space-y-4">
        <p className="text-sm text-error">Este enlace no es válido o le falta el token de recuperación.</p>
        <Link href="/forgot-password" className="block text-center text-sm font-medium text-primary hover:underline">
          Solicitar un nuevo enlace
        </Link>
      </div>
    );
  }

  if (resetPassword.isSuccess) {
    return (
      <div className="space-y-4">
        <p className="text-sm text-success">Tu contraseña se actualizó correctamente.</p>
        <Button className="w-full" onClick={() => router.push("/login")}>
          Ir a iniciar sesión
        </Button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div className="space-y-2">
        <Label htmlFor="new_password">Nueva contraseña</Label>
        <Input
          id="new_password"
          type="password"
          autoComplete="new-password"
          required
          minLength={8}
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          placeholder="Mínimo 8 caracteres"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="confirm_password">Confirmar contraseña</Label>
        <Input
          id="confirm_password"
          type="password"
          autoComplete="new-password"
          required
          minLength={8}
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Repite la contraseña"
        />
      </div>

      {formError && (
        <p role="alert" className="text-sm text-error">
          {formError}
        </p>
      )}

      <Button type="submit" className="w-full" disabled={resetPassword.isPending}>
        {resetPassword.isPending ? "Guardando..." : "Restablecer contraseña"}
      </Button>
    </form>
  );
}

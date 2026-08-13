"use client";

import { useState, type FormEvent } from "react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useForgotPassword } from "@/features/auth/hooks/use-forgot-password";
import { ApiError } from "@/lib/api-client";

export function ForgotPasswordForm() {
  const forgotPassword = useForgotPassword();
  const [email, setEmail] = useState("");
  const [formError, setFormError] = useState<string | null>(null);

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setFormError(null);
    forgotPassword.mutate(
      { email },
      {
        onError: (error) => {
          setFormError(
            error instanceof ApiError ? error.message : "No se pudo procesar la solicitud. Intenta de nuevo."
          );
        },
      }
    );
  }

  // Respuesta genérica ya recibida: mostramos el mensaje de éxito
  // (el mismo exista o no el email, por diseño del backend).
  if (forgotPassword.isSuccess) {
    const devToken = forgotPassword.data.dev_reset_token;
    return (
      <div className="space-y-4">
        <p className="text-sm text-foreground">{forgotPassword.data.message}</p>

        {devToken && (
          <div className="rounded border border-warning/40 bg-warning/10 p-4 text-sm">
            <p className="mb-2 font-medium text-warning">Modo desarrollo</p>
            <p className="mb-3 text-foreground-muted">
              No hay servicio de email conectado todavía, así que el enlace se muestra aquí solo para pruebas:
            </p>
            <Link
              href={`/reset-password?token=${encodeURIComponent(devToken)}`}
              className="break-all font-medium text-primary hover:underline"
            >
              Restablecer contraseña →
            </Link>
          </div>
        )}

        <Link href="/login" className="block text-center text-sm font-medium text-primary hover:underline">
          Volver a iniciar sesión
        </Link>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div className="space-y-2">
        <Label htmlFor="email">Correo</Label>
        <Input
          id="email"
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="tucorreo@upmh.edu"
        />
      </div>

      {formError && (
        <p role="alert" className="text-sm text-error">
          {formError}
        </p>
      )}

      <Button type="submit" className="w-full" disabled={forgotPassword.isPending}>
        {forgotPassword.isPending ? "Enviando..." : "Enviar enlace de recuperación"}
      </Button>
    </form>
  );
}

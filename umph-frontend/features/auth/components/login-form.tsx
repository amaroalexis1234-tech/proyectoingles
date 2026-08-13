"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useLogin } from "@/features/auth/hooks/use-login";
import { ApiError } from "@/lib/api-client";

export function LoginForm() {
  const router = useRouter();
  const login = useLogin();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [formError, setFormError] = useState<string | null>(null);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setFormError(null);

    login.mutate(
      {
        email,
        password,
      },
      {
        onSuccess: (data) => {
          router.push(data.user.role === "teacher" ? "/teacher/students" : "/dashboard");
        },

        onError: (error) => {
          setFormError(
            error instanceof ApiError
              ? error.message
              : "No se pudo iniciar sesión. Intenta de nuevo."
          );
        },
      }
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Correo */}
      <div className="space-y-2">
        <Label htmlFor="email">Correo</Label>

        <Input
          id="email"
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          placeholder="tucorreo@upmh.edu"
        />
      </div>

      {/* Contraseña */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label htmlFor="password">Contraseña</Label>

          <Link
            href="/forgot-password"
            className="text-sm text-primary hover:underline"
          >
            ¿Olvidaste tu contraseña?
          </Link>
        </div>

        <Input
          id="password"
          type="password"
          autoComplete="current-password"
          required
          minLength={8}
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          placeholder="••••••••"
        />
      </div>

      {/* Error */}
      {formError && (
        <p role="alert" className="text-sm text-error">
          {formError}
        </p>
      )}

      {/* Botón */}
      <Button
        type="submit"
        className="w-full"
        disabled={login.isPending}
      >
        {login.isPending ? "Ingresando..." : "Iniciar sesión"}
      </Button>
    </form>
  );
}

"use client";

import { useState, type FormEvent } from "react";

import { Button } from "@/components/ui/button";
import { Dialog, DialogCloseButton, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useChangePassword } from "@/features/profile/hooks/use-change-password";
import { ApiError } from "@/lib/api-client";

export function ChangePasswordDialog() {
  const changePassword = useChangePassword();

  const [open, setOpen] = useState(false);
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [formError, setFormError] = useState<string | null>(null);

  function reset() {
    setCurrentPassword("");
    setNewPassword("");
    setConfirmPassword("");
    setFormError(null);
    changePassword.reset();
  }

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setFormError(null);

    if (newPassword !== confirmPassword) {
      setFormError("Las contraseñas no coinciden.");
      return;
    }

    changePassword.mutate(
      { currentPassword, newPassword },
      {
        onError: (error) => {
          setFormError(
            error instanceof ApiError ? error.message : "No se pudo cambiar la contraseña. Intenta de nuevo."
          );
        },
      }
    );
  }

  return (
    <Dialog
      open={open}
      onOpenChange={(next) => {
        setOpen(next);
        if (next) reset();
      }}
    >
      <DialogTrigger asChild>
        <button className="flex w-full items-center justify-between text-left">
          <div>
            <p className="text-sm font-medium text-foreground">Cambiar contraseña</p>
            <p className="text-sm text-foreground-muted">Actualiza tu contraseña de acceso.</p>
          </div>
          <span aria-hidden="true" className="text-foreground-muted">
            ›
          </span>
        </button>
      </DialogTrigger>
      <DialogContent className="flex items-center justify-center bg-transparent p-4">
        <div className="w-full max-w-sm rounded border border-border bg-surface p-6 shadow-card">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-foreground">Cambiar contraseña</h2>
            <DialogCloseButton />
          </div>

          {changePassword.isSuccess ? (
            <p className="text-sm text-success">Tu contraseña se actualizó correctamente.</p>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="current_password">Contraseña actual</Label>
                <Input
                  id="current_password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                />
              </div>
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
                <Label htmlFor="confirm_password">Confirmar nueva contraseña</Label>
                <Input
                  id="confirm_password"
                  type="password"
                  autoComplete="new-password"
                  required
                  minLength={8}
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </div>

              {formError && (
                <p role="alert" className="text-sm text-error">
                  {formError}
                </p>
              )}

              <Button type="submit" className="w-full" disabled={changePassword.isPending}>
                {changePassword.isPending ? "Guardando..." : "Cambiar contraseña"}
              </Button>
            </form>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}

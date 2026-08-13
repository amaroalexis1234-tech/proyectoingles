"use client";

import { useState, type FormEvent } from "react";
import { LogOut } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { ThemeToggle } from "@/components/theme/theme-toggle";
import { useLogout } from "@/features/auth/hooks/use-logout";
import { ChangePasswordDialog } from "@/features/profile/components/change-password-dialog";
import { ExportProgressButton } from "@/features/profile/components/export-progress-button";
import { useUpdateProfile } from "@/features/profile/hooks/use-update-profile";
import { useSessionStore } from "@/store/session-store";

export default function SettingsPage() {
  const user = useSessionStore((s) => s.user);
  const updateProfile = useUpdateProfile();
  const logout = useLogout();

  const [fullName, setFullName] = useState(user?.full_name ?? "");
  const [saved, setSaved] = useState(false);

  // Decorativos: no hay backend/i18n/preferencias para esto todavia --
  // mismo criterio que los botones de OAuth del Modulo 1.
  const [notifications, setNotifications] = useState(true);
  const [sounds, setSounds] = useState(true);

  function handleAccountSubmit(event: FormEvent) {
    event.preventDefault();
    setSaved(false);
    updateProfile.mutate(fullName, { onSuccess: () => setSaved(true) });
  }

  return (
    <div className="animate-fade-in mx-auto max-w-lg space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Configuración</h1>
        <p className="text-sm text-foreground-muted">Personaliza tu cuenta y preferencias.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Cuenta</CardTitle>
          <CardDescription>Actualiza tu información personal.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleAccountSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="full_name">Nombre completo</Label>
              <Input
                id="full_name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                minLength={2}
                required
              />
            </div>
            {saved && <p className="text-sm text-success">Guardado.</p>}
            <Button type="submit" size="sm" disabled={updateProfile.isPending}>
              {updateProfile.isPending ? "Guardando..." : "Guardar cambios"}
            </Button>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="flex items-center justify-between pt-2">
          <div>
            <p className="text-sm font-medium text-foreground">Idioma</p>
            <p className="text-sm text-foreground-muted">Selecciona el idioma de la aplicación.</p>
          </div>
          {/* No funcional: no hay i18n implementado todavía. */}
          <select
            disabled
            className="rounded border border-border bg-background px-3 py-1.5 text-sm text-foreground-muted"
            defaultValue="es"
          >
            <option value="es">Español</option>
          </select>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="flex items-center justify-between pt-2">
          <div>
            <p className="text-sm font-medium text-foreground">Tema</p>
            <p className="text-sm text-foreground-muted">Selecciona el tema de la aplicación.</p>
          </div>
          <ThemeToggle />
        </CardContent>
      </Card>

      <Card>
        <CardContent className="space-y-4 pt-2">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-foreground">Notificaciones</p>
              <p className="text-sm text-foreground-muted">Recibe notificaciones sobre tu progreso.</p>
            </div>
            <Switch checked={notifications} onCheckedChange={setNotifications} aria-label="Notificaciones" />
          </div>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-foreground">Sonidos</p>
              <p className="text-sm text-foreground-muted">Activa o desactiva los sonidos.</p>
            </div>
            <Switch checked={sounds} onCheckedChange={setSounds} aria-label="Sonidos" />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="pt-2">
          <ChangePasswordDialog />
        </CardContent>
      </Card>

      <Card>
        <CardContent className="flex items-center justify-between pt-2">
          <div>
            <p className="text-sm font-medium text-foreground">Privacidad</p>
            <p className="text-sm text-foreground-muted">Controla tu información y datos personales.</p>
          </div>
          {/* Decorativo: no hay preferencias de privacidad implementadas todavía. */}
          <span aria-hidden="true" className="text-foreground-muted">
            ›
          </span>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="pt-2">
          <ExportProgressButton />
        </CardContent>
      </Card>

      <Button variant="secondary" className="w-full" onClick={logout}>
        <LogOut className="h-4 w-4" />
        Cerrar sesión
      </Button>
    </div>
  );
}

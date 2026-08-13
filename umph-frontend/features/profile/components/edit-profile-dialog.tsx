"use client";

import { useState, type FormEvent } from "react";

import { Button } from "@/components/ui/button";
import { Dialog, DialogCloseButton, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useUpdateProfile } from "@/features/profile/hooks/use-update-profile";
import { useSessionStore } from "@/store/session-store";

export function EditProfileDialog() {
  const user = useSessionStore((s) => s.user);
  const updateProfile = useUpdateProfile();

  const [open, setOpen] = useState(false);
  const [fullName, setFullName] = useState(user?.full_name ?? "");
  const [saved, setSaved] = useState(false);

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setSaved(false);
    updateProfile.mutate(fullName, { onSuccess: () => setSaved(true) });
  }

  return (
    <Dialog
      open={open}
      onOpenChange={(next) => {
        setOpen(next);
        if (next) {
          setFullName(user?.full_name ?? "");
          setSaved(false);
        }
      }}
    >
      <DialogTrigger asChild>
        <Button size="sm">Editar perfil</Button>
      </DialogTrigger>
      <DialogContent className="flex items-center justify-center bg-transparent p-4">
        <div className="w-full max-w-sm rounded border border-border bg-surface p-6 shadow-card">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-foreground">Editar perfil</h2>
            <DialogCloseButton />
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
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
            <Button type="submit" className="w-full" disabled={updateProfile.isPending}>
              {updateProfile.isPending ? "Guardando..." : "Guardar cambios"}
            </Button>
          </form>
        </div>
      </DialogContent>
    </Dialog>
  );
}

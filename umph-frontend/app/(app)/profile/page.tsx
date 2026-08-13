"use client";

import { useRef, useState, type ChangeEvent } from "react";
import type { LucideIcon } from "lucide-react";
import { ClipboardCheck, Clock, Loader2, Monitor, Pencil, Target } from "lucide-react";

import { Avatar } from "@/components/ui/avatar";
import { Card } from "@/components/ui/card";
import { EditProfileDialog } from "@/features/profile/components/edit-profile-dialog";
import { useUploadAvatar } from "@/features/profile/hooks/use-upload-avatar";
import { useDashboardSummary } from "@/features/progress/hooks/use-dashboard-summary";
import { useStudyStatistics } from "@/features/progress/hooks/use-study-statistics";
import { ApiError } from "@/lib/api-client";
import { useSessionStore } from "@/store/session-store";

// Nombres oficiales de las bandas CEFR (Marco Comun Europeo de Referencia) --
// no son una invencion, es la nomenclatura estandar del marco.
const CEFR_BAND_NAMES: Record<string, string> = {
  A1: "Principiante",
  A2: "Elemental",
  B1: "Intermedio",
  B2: "Intermedio alto",
  C1: "Avanzado",
  C2: "Dominio",
};

function formatStudyTime(totalSeconds: number): string {
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  if (hours === 0) return `${minutes}m`;
  return `${hours}h ${minutes}m`;
}

interface Tile {
  icon: LucideIcon;
  label: string;
  value: string;
  color: string;
}

export default function ProfilePage() {
  const user = useSessionStore((s) => s.user);
  const { data: summary } = useDashboardSummary();
  const { data: stats } = useStudyStatistics();
  const uploadAvatar = useUploadAvatar();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [avatarError, setAvatarError] = useState<string | null>(null);

  function handleAvatarClick() {
    fileInputRef.current?.click();
  }

  function handleAvatarChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    event.target.value = ""; // permite volver a elegir el mismo archivo despues
    if (!file) return;

    setAvatarError(null);
    uploadAvatar.mutate(file, {
      onError: (error) => {
        setAvatarError(error instanceof ApiError ? error.message : "No se pudo subir la foto. Intenta de nuevo.");
      },
    });
  }

  const tiles: Tile[] = stats
    ? [
        { icon: ClipboardCheck, label: "Mini Tests completados", value: String(stats.completed_mini_tests), color: "text-primary bg-primary/10" },
        { icon: Monitor, label: "Simuladores realizados", value: String(stats.completed_simulators), color: "text-accent-green bg-accent-green/10" },
        { icon: Clock, label: "Tiempo estudiado", value: formatStudyTime(stats.study_time_seconds), color: "text-accent-purple bg-accent-purple/10" },
        { icon: Target, label: "Precisión promedio", value: stats.accuracy_percent != null ? `${stats.accuracy_percent}%` : "—", color: "text-accent-orange bg-accent-orange/10" },
      ]
    : [];

  return (
    <div className="animate-fade-in mx-auto max-w-2xl space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Mi Perfil</h1>
        <p className="text-sm text-foreground-muted">Información personal y tu progreso en UPMH English Prep.</p>
      </div>

      <Card>
        <div className="flex flex-col items-center gap-4 sm:flex-row">
          <div className="relative">
            <Avatar fullName={user?.full_name} avatarUrl={user?.avatar_url} size="lg" />
            <input
              ref={fileInputRef}
              type="file"
              accept="image/png,image/jpeg,image/webp,image/gif"
              className="hidden"
              onChange={handleAvatarChange}
            />
            <button
              onClick={handleAvatarClick}
              disabled={uploadAvatar.isPending}
              title="Cambiar foto de perfil"
              className="absolute -bottom-1 -right-1 flex h-7 w-7 items-center justify-center rounded-full bg-surface text-foreground-muted transition-colors hover:bg-primary hover:text-primary-foreground disabled:opacity-50"
            >
              {uploadAvatar.isPending ? (
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
              ) : (
                <Pencil className="h-3.5 w-3.5" />
              )}
            </button>
          </div>

          <div className="flex-1 text-center sm:text-left">
            <p className="text-lg font-semibold text-foreground">{user?.full_name}</p>
            {avatarError && <p className="text-sm text-error">{avatarError}</p>}
            <p className="mb-2 text-sm text-foreground-muted">Nivel de inglés</p>
            <p className="font-medium text-foreground">
              {summary?.level
                ? `${summary.level.cefr_band} ${CEFR_BAND_NAMES[summary.level.cefr_band] ?? ""}`
                : "Aún sin evaluar"}
            </p>

            <div className="mt-3 flex justify-center gap-4 border-t border-border pt-3 sm:justify-start">
              <div>
                <p className="text-sm font-semibold text-foreground">{summary?.current_xp ?? 0} XP Total</p>
              </div>
              <div>
                <p className="text-sm font-semibold text-foreground">{summary?.streak_days ?? 0} días</p>
              </div>
            </div>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-2 gap-3">
        {tiles.map(({ icon: Icon, label, value, color }) => (
          <Card key={label} className="flex items-center gap-3 p-4">
            <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded ${color}`}>
              <Icon className="h-5 w-5" />
            </div>
            <div className="min-w-0">
              <p className="truncate text-lg font-semibold text-foreground">{value}</p>
              <p className="truncate text-xs text-foreground-muted">{label}</p>
            </div>
          </Card>
        ))}
      </div>

      <Card className="flex flex-col items-center justify-between gap-3 sm:flex-row">
        <div className="text-center sm:text-left">
          <p className="text-sm font-medium text-foreground">Actualiza tu información personal</p>
          <p className="text-sm text-foreground-muted">Mantén tus datos al día para una mejor experiencia.</p>
        </div>
        <EditProfileDialog />
      </Card>
    </div>
  );
}

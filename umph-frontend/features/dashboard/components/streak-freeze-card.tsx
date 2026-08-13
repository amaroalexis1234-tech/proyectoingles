"use client";

import { useState } from "react";
import { Snowflake } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useActivateStreakFreeze } from "@/features/progress/hooks/use-streak-freeze";
import { ApiError } from "@/lib/api-client";

interface StreakFreezeCardProps {
  streakDays: number;
  freezeAvailable: boolean;
}

/** Solo tiene sentido si ya hay una racha real que proteger. */
export function StreakFreezeCard({ streakDays, freezeAvailable }: StreakFreezeCardProps) {
  const activateFreeze = useActivateStreakFreeze();
  const [error, setError] = useState<string | null>(null);

  if (streakDays < 1) return null;

  function handleFreeze() {
    setError(null);
    activateFreeze.mutate(undefined, {
      onError: (err) => {
        setError(err instanceof ApiError ? err.message : "No se pudo congelar la racha. Intenta de nuevo.");
      },
    });
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <Snowflake className="h-4 w-4 text-foreground-muted" />
          Congelar racha
        </CardTitle>
        <CardDescription>
          {freezeAvailable
            ? "¿No vas a poder practicar hoy? Protege tu racha una vez al mes."
            : "Ya usaste tu congelamiento de este mes."}
        </CardDescription>
      </CardHeader>
      <CardContent>
        {activateFreeze.isSuccess ? (
          <p className="text-sm text-success">Racha protegida por hoy.</p>
        ) : (
          <Button
            size="sm"
            variant="secondary"
            className="w-full"
            disabled={!freezeAvailable || activateFreeze.isPending}
            onClick={handleFreeze}
          >
            {activateFreeze.isPending ? "Congelando..." : "Congelar racha por hoy"}
          </Button>
        )}
        {error && <p className="mt-2 text-xs text-error">{error}</p>}
      </CardContent>
    </Card>
  );
}

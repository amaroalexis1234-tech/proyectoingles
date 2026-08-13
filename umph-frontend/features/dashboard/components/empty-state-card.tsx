import type { LucideIcon } from "lucide-react";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

interface EmptyStateCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
  hint: string;
}

/**
 * Estado honesto de "aun no hay datos": Weak Skills y Quick Practice
 * necesitan intentos reales de ejercicios (modulo Learning) para
 * calcularse. Mientras eso no exista, se muestra esto -- nunca numeros
 * inventados.
 */
export function EmptyStateCard({ icon: Icon, title, description, hint }: EmptyStateCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <Icon className="h-4 w-4 text-foreground-muted" />
          {title}
        </CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-foreground-muted">{hint}</p>
      </CardContent>
    </Card>
  );
}

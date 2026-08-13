import type { LucideIcon } from "lucide-react";

import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

type FeatureColor = "blue" | "green" | "purple" | "orange";

// Clases completas y estaticas (no interpoladas) para que Tailwind las detecte en build.
const COLOR_STYLES: Record<FeatureColor, { icon: string; underline: string }> = {
  blue: { icon: "bg-primary/10 text-primary", underline: "bg-primary" },
  green: { icon: "bg-accent-green/10 text-accent-green", underline: "bg-accent-green" },
  purple: { icon: "bg-accent-purple/10 text-accent-purple", underline: "bg-accent-purple" },
  orange: { icon: "bg-accent-orange/10 text-accent-orange", underline: "bg-accent-orange" },
};

interface FeatureCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
  color: FeatureColor;
}

export function FeatureCard({ icon: Icon, title, description, color }: FeatureCardProps) {
  const styles = COLOR_STYLES[color];

  return (
    <Card className="space-y-4">
      <div className={cn("flex h-11 w-11 items-center justify-center rounded", styles.icon)}>
        <Icon className="h-5 w-5" />
      </div>

      <div className="space-y-1.5">
        <h3 className="font-semibold text-foreground">{title}</h3>
        <p className="text-sm text-foreground-muted">{description}</p>
      </div>

      <div className={cn("h-1 w-10 rounded-full", styles.underline)} />
    </Card>
  );
}

import { BACKEND_ORIGIN } from "@/lib/api-client";
import { cn } from "@/lib/utils";

const SIZE_CLASSES = {
  sm: "h-8 w-8 text-sm",
  md: "h-14 w-14 text-lg",
  lg: "h-20 w-20 text-2xl",
} as const;

export function initialsFor(fullName: string | undefined | null): string {
  if (!fullName) return "?";
  const parts = fullName.trim().split(/\s+/);
  const first = parts[0]?.[0] ?? "";
  const second = parts.length > 1 ? parts[1]?.[0] ?? "" : "";
  return (first + second).toUpperCase();
}

interface AvatarProps {
  fullName: string | undefined | null;
  avatarUrl: string | null | undefined;
  size?: keyof typeof SIZE_CLASSES;
  className?: string;
}

/** Foto real si el usuario subio una, si no iniciales -- un solo lugar decide esto. */
export function Avatar({ fullName, avatarUrl, size = "sm", className }: AvatarProps) {
  if (avatarUrl) {
    return (
      // eslint-disable-next-line @next/next/no-img-element -- imagen subida por el usuario, no un asset estatico del build
      <img
        src={`${BACKEND_ORIGIN}${avatarUrl}`}
        alt={fullName ?? "Avatar"}
        className={cn("shrink-0 rounded-full object-cover", SIZE_CLASSES[size], className)}
      />
    );
  }

  return (
    <span
      className={cn(
        "flex shrink-0 items-center justify-center rounded-full bg-primary font-semibold text-primary-foreground",
        SIZE_CLASSES[size],
        className
      )}
    >
      {initialsFor(fullName)}
    </span>
  );
}

import Link from "next/link";

import { AuthIllustration } from "./auth-illustration";

export function AuthAsidePanel() {
  return (
    <div className="hidden flex-col justify-between bg-auth-aside p-10 text-auth-aside-foreground lg:flex">
      <Link href="/" className="text-lg font-semibold tracking-tight">
        UPMH <span className="opacity-80">English Prep</span>
      </Link>

      <div className="space-y-8">
        <AuthIllustration />

        <div className="space-y-2 text-center">
          <h2 className="text-2xl font-semibold tracking-tight">Tu preparación, nuestro objetivo</h2>
          <p className="mx-auto max-w-sm text-sm text-auth-aside-foreground/80">
            Únete a miles de estudiantes que están alcanzando sus metas con nuestra plataforma.
          </p>
        </div>
      </div>

      <div className="flex justify-center gap-2">
        <span className="h-1.5 w-6 rounded-full bg-white" />
        <span className="h-1.5 w-1.5 rounded-full bg-white/40" />
        <span className="h-1.5 w-1.5 rounded-full bg-white/40" />
      </div>
    </div>
  );
}

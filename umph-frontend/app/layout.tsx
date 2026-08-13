import type { Metadata } from "next";

import { Providers } from "@/app/providers";
import "./globals.css";

export const metadata: Metadata = {
  title: "UPMH English Prep",
  description: "Preparación para el examen TOEFL ITP de la UPMH",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    // suppressHydrationWarning: next-themes muta la clase de <html> antes de
    // que React hidrate (evita flash de tema incorrecto), lo que genera un
    // mismatch esperado en este elemento -- no es un supresor general.
    <html lang="es" suppressHydrationWarning>
      <body className="font-sans antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

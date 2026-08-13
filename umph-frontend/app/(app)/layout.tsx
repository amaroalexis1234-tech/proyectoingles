import { Header } from "@/components/layout/header";
import { MobileNav } from "@/components/layout/mobile-nav";
import { Sidebar } from "@/components/layout/sidebar";

/**
 * Layout compartido por todas las pantallas protegidas. Sidebar (desktop)
 * y MobileNav (mobile) muestran la misma navegacion, solo cambia la
 * presentacion segun el tamaño de pantalla -- ningun modulo vuelve a
 * definir su propia navegacion.
 */
export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />
      <div className="flex flex-1 flex-col">
        <Header />
        <main className="flex-1 pb-16 md:pb-0">{children}</main>
      </div>
      <MobileNav />
    </div>
  );
}

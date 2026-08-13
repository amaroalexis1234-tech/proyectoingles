import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PROTECTED_PREFIXES = ["/dashboard", "/practice", "/evaluations", "/results", "/stats", "/profile", "/history", "/settings", "/teacher"];

/**
 * Proteccion ligera: verifica solo la cookie marcador "has_session" que
 * pone el frontend (no la cookie de refresh, que vive en el dominio del
 * backend y nunca es visible aqui). No valida el token en si -- eso lo
 * hace el backend en cada request; esto solo evita cargar una pantalla
 * protegida cuando es obvio que no hay sesion.
 */
export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const isProtected = PROTECTED_PREFIXES.some((prefix) => pathname.startsWith(prefix));

  if (isProtected && !request.cookies.has("has_session")) {
    const loginUrl = new URL("/login", request.url);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/dashboard/:path*",
    "/practice/:path*",
    "/evaluations/:path*",
    "/results/:path*",
    "/stats/:path*",
    "/profile/:path*",
    "/history/:path*",
    "/settings/:path*",
    "/teacher/:path*",
  ],
};

import { useSessionStore } from "@/store/session-store";
import type { AccessTokenResponse } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

// Origen sin el sufijo /api -- para armar URLs de archivos estaticos
// (ej. avatar_url) que el backend sirve fuera del prefijo de la API.
export const BACKEND_ORIGIN = API_BASE_URL.replace(/\/api\/?$/, "");

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

interface RequestOptions {
  method?: "GET" | "POST" | "PATCH" | "DELETE";
  body?: unknown;
  /** false para endpoints publicos (login/register): evita el intento de refresh en un 401 esperado. */
  auth?: boolean;
}

async function rawRequest<T>(path: string, options: RequestOptions): Promise<T> {
  const { accessToken } = useSessionStore.getState();
  // FormData (ej. subida de avatar): el navegador arma su propio
  // Content-Type con boundary -- fijarlo a mano rompe el parseo multipart.
  const isFormData = options.body instanceof FormData;

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method ?? "GET",
    headers: {
      ...(isFormData ? {} : { "Content-Type": "application/json" }),
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
    },
    // credentials: "include" es obligatorio para que el navegador mande
    // la cookie httpOnly del refresh token al backend (dominio distinto en dev).
    credentials: "include",
    body: options.body ? (isFormData ? (options.body as FormData) : JSON.stringify(options.body)) : undefined,
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({ detail: response.statusText }));
    throw new ApiError(data.detail ?? "Error de red", response.status);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

/**
 * Intenta renovar el access token via /auth/refresh (cookie httpOnly).
 * Devuelve true si lo logro, false si la sesion ya no es valida.
 */
async function tryRefreshSession(): Promise<boolean> {
  try {
    const data = await rawRequest<AccessTokenResponse>("/auth/refresh", {
      method: "POST",
      auth: false,
    });
    useSessionStore.getState().setSession(data.user, data.access_token);
    return true;
  } catch {
    useSessionStore.getState().clearSession();
    return false;
  }
}

export async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  try {
    return await rawRequest<T>(path, options);
  } catch (error) {
    const isAuthEndpoint = options.auth === false;
    if (error instanceof ApiError && error.status === 401 && !isAuthEndpoint) {
      const refreshed = await tryRefreshSession();
      if (refreshed) {
        return rawRequest<T>(path, options);
      }
    }
    throw error;
  }
}

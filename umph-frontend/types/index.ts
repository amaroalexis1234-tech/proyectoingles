// Tipos compartidos entre modulos. Reflejan 1:1 los schemas Pydantic del
// backend (UserRead, etc.) para que un cambio ahi obligue a actualizar aqui
// tambien -- si un dia usamos codegen desde el OpenAPI, este archivo se
// vuelve el objetivo a reemplazar.

export interface User {
  id: string;
  email: string;
  full_name: string;
  current_xp: number;
  role: "student" | "teacher";
  avatar_url: string | null;
}

export interface AccessTokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface ForgotPasswordResponse {
  message: string;
  dev_reset_token: string | null;
}

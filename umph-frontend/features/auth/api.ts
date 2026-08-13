import { apiRequest } from "@/lib/api-client";
import type { AccessTokenResponse, ForgotPasswordResponse } from "@/types";

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
  full_name: string;
}

export function loginRequest(payload: LoginPayload) {
  return apiRequest<AccessTokenResponse>("/auth/login", {
    method: "POST",
    body: payload,
    auth: false,
  });
}

export function registerRequest(payload: RegisterPayload) {
  return apiRequest<AccessTokenResponse>("/auth/register", {
    method: "POST",
    body: payload,
    auth: false,
  });
}

export interface ForgotPasswordPayload {
  email: string;
}

export interface ResetPasswordPayload {
  token: string;
  new_password: string;
}

export function forgotPasswordRequest(payload: ForgotPasswordPayload) {
  return apiRequest<ForgotPasswordResponse>("/auth/forgot-password", {
    method: "POST",
    body: payload,
    auth: false,
  });
}

export function resetPasswordRequest(payload: ResetPasswordPayload) {
  return apiRequest<void>("/auth/reset-password", {
    method: "POST",
    body: payload,
    auth: false,
  });
}

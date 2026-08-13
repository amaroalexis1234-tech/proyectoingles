import { apiRequest } from "@/lib/api-client";
import type { User } from "@/types";

export function updateProfile(fullName: string) {
  return apiRequest<User>("/auth/me", {
    method: "PATCH",
    body: { full_name: fullName },
  });
}

export function changePassword(currentPassword: string, newPassword: string) {
  return apiRequest<void>("/auth/change-password", {
    method: "POST",
    body: { current_password: currentPassword, new_password: newPassword },
  });
}

export function uploadAvatar(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  return apiRequest<User>("/auth/me/avatar", { method: "POST", body: formData });
}

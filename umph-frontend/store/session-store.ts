"use client";

import { create } from "zustand";

import type { User } from "@/types";

interface SessionState {
  user: User | null;
  accessToken: string | null;
  setSession: (user: User, accessToken: string) => void;
  updateAccessToken: (accessToken: string) => void;
  clearSession: () => void;
}

const SESSION_MARKER_COOKIE = "has_session";

function setSessionMarker() {
  document.cookie =
    `${SESSION_MARKER_COOKIE}=1; path=/; max-age=${60 * 60 * 24 * 7}; samesite=lax`;
}

function clearSessionMarker() {
  document.cookie =
    `${SESSION_MARKER_COOKIE}=; path=/; max-age=0`;
}

export const useSessionStore = create<SessionState>((set) => ({
  user: null,
  accessToken: null,

  setSession: (user, accessToken) => {
    setSessionMarker();

    set({
      user,
      accessToken,
    });
  },

  updateAccessToken: (accessToken) => {
    set({ accessToken });
  },

  clearSession: () => {
    clearSessionMarker();

    set({
      user: null,
      accessToken: null,
    });
  },
}));
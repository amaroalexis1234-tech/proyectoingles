import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 min: evita refetch agresivo en datos que no cambian a cada segundo
      retry: 1,
    },
  },
});

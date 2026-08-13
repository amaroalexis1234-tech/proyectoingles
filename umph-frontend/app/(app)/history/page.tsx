"use client";

import { AttemptHistoryList } from "@/features/progress/components/attempt-history-list";
import { useHistory } from "@/features/progress/hooks/use-history";

export default function HistoryPage() {
  const { data: history, isLoading } = useHistory();

  if (isLoading || !history) {
    return (
      <div className="p-6">
        <div className="h-6 w-40 animate-pulse rounded bg-surface" />
      </div>
    );
  }

  return (
    <div className="animate-fade-in space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Historial</h1>
        <p className="text-sm text-foreground-muted">Todas tus evaluaciones completadas.</p>
      </div>

      <AttemptHistoryList attempts={history} />
    </div>
  );
}

"use client";

import Link from "next/link";
import { BookOpen } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import { useReadingPassages } from "@/features/learning/hooks/use-reading-passages";

export default function ReadingPassageListPage() {
  const { data: passages, isLoading } = useReadingPassages();

  if (isLoading || !passages) {
    return (
      <div className="p-6">
        <div className="h-6 w-40 animate-pulse rounded bg-surface" />
      </div>
    );
  }

  return (
    <div className="animate-fade-in space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Reading</h1>
        <p className="text-sm text-foreground-muted">Elige un passage para practicar.</p>
      </div>

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {passages.map((passage) => (
          <Link key={passage.id} href={`/practice/reading/${passage.id}`}>
            <Card className="h-full transition-colors hover:border-primary">
              <CardContent className="flex items-center gap-3 space-y-0 pt-2">
                <BookOpen className="h-5 w-5 shrink-0 text-primary" />
                <span className="text-sm font-medium text-foreground">{passage.title}</span>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}

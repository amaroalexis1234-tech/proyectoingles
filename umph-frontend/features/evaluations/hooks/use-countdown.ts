import { useEffect, useRef, useState } from "react";

/**
 * Cuenta regresiva en segundos. onExpire se llama una sola vez al llegar
 * a cero (uso: auto-finalizar el Simulador cuando se acaba el tiempo).
 */
export function useCountdown(initialSeconds: number | null, onExpire: () => void) {
  const [secondsLeft, setSecondsLeft] = useState(initialSeconds ?? 0);
  const hasExpiredRef = useRef(false);

  useEffect(() => {
    if (initialSeconds == null) return;
    setSecondsLeft(initialSeconds);
    hasExpiredRef.current = false;
  }, [initialSeconds]);

  useEffect(() => {
    if (initialSeconds == null) return;

    const interval = setInterval(() => {
      setSecondsLeft((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          if (!hasExpiredRef.current) {
            hasExpiredRef.current = true;
            onExpire();
          }
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [initialSeconds, onExpire]);

  const minutes = Math.floor(secondsLeft / 60);
  const seconds = secondsLeft % 60;
  const formatted = `${minutes}:${seconds.toString().padStart(2, "0")}`;

  return { secondsLeft, formatted };
}

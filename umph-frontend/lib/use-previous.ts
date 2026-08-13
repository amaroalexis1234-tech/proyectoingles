import { useEffect, useRef } from "react";

/** Devuelve el valor del render anterior (undefined en el primer render). */
export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);
  useEffect(() => {
    ref.current = value;
  });
  return ref.current;
}

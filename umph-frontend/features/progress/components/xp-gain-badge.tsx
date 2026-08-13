"use client";

import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

/**
 * Pop animado al ganar XP (respuesta correcta, examen completado). Entrada
 * con spring -- se ve vivo/dinamico en vez de aparecer de golpe como texto plano.
 */
export function XpGainBadge({ amount }: { amount: number }) {
  return (
    <motion.span
      initial={{ scale: 0, opacity: 0, y: 8 }}
      animate={{ scale: 1, opacity: 1, y: 0 }}
      transition={{ type: "spring", stiffness: 500, damping: 15 }}
      className="inline-flex items-center gap-1 rounded-full bg-success/10 px-2.5 py-1 text-sm font-semibold text-success"
    >
      <Sparkles className="h-3.5 w-3.5" />+{amount} XP
    </motion.span>
  );
}

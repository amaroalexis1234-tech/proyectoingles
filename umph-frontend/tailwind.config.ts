import type { Config } from "tailwindcss";

// Paleta y tokens tomados directamente del design system aprobado.
// Nunca se agregan colores nuevos aqui sin que primero se actualice el
// documento de diseño — la fuente de verdad visual vive ahi, no en el codigo.
const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{ts,tsx}",
    "./features/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        surface: "var(--surface)", // "Cards" en el doc de diseño
        primary: {
          DEFAULT: "var(--primary)",
          foreground: "var(--primary-foreground)",
        },
        success: "var(--success)",
        error: "var(--error)",
        warning: "var(--warning)",
        border: "var(--border)",
        foreground: {
          DEFAULT: "var(--text-primary)",
          muted: "var(--text-secondary)",
        },
        // Colores de marca no-semanticos (secciones/categorias), deliberadamente
        // separados de success/warning que son semanticos de estado.
        accent: {
          green: "var(--accent-green)",
          purple: "var(--accent-purple)",
          orange: "var(--accent-orange)",
        },
        "auth-aside": {
          DEFAULT: "var(--auth-aside-bg)",
          foreground: "var(--auth-aside-foreground)",
        },
      },
      borderRadius: {
        DEFAULT: "16px", // unico radius de todo el sistema, segun el design doc
      },
      boxShadow: {
        card: "var(--shadow-card)",
      },
      fontFamily: {
        // Pila de fuentes del sistema: moderna, legible, sin dependencia de
        // descarga externa en build time (mas resistente en CI sin salida a internet).
        sans: [
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Arial",
          "sans-serif",
        ],
      },
      keyframes: {
        "fade-in": {
          from: { opacity: "0", transform: "translateY(4px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        "fade-in": "fade-in 0.35s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;

#!/usr/bin/env bash
# Deja el frontend listo para correr: dependencias + .env.local
set -e

echo "== 1/2: Instalando dependencias =="
npm install

echo "== 2/2: Generando .env.local (si no existe) =="
if [ ! -f ".env.local" ]; then
    cp .env.example .env.local
    echo ".env.local creado."
else
    echo ".env.local ya existe, no se modifica."
fi

echo ""
echo "Listo. Para levantar el servidor:"
echo "  npm run dev"

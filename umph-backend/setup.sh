#!/usr/bin/env bash
# Deja el backend listo para correr: venv + dependencias + .env + migraciones.
# Uso: ./setup.sh   (desde umph-backend/)
set -e

echo "== 1/5: Creando entorno virtual =="
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

echo "== 2/5: Activando entorno virtual =="
source venv/bin/activate

echo "== 3/5: Instalando dependencias =="
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "== 4/5: Generando .env (si no existe) =="
python scripts/init_env.py

echo "== 5/5: Esperando MySQL y aplicando migraciones =="
python -m scripts.wait_for_db
alembic upgrade head

echo ""
echo "Listo. Para levantar el servidor:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"

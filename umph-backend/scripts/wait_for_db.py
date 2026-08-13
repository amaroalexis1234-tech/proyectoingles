"""
Espera hasta que MySQL acepte conexiones antes de correr alembic.
Sin esto, si acabas de levantar el contenedor con docker compose up,
el primer intento de conexion casi siempre falla porque MySQL todavia
esta inicializando.
"""
import sys
import time

import pymysql

from app.core.config import settings

MAX_ATTEMPTS = 20
WAIT_SECONDS = 2


def parse_mysql_url(url: str) -> dict:
    # mysql+pymysql://user:password@host:port/dbname
    without_scheme = url.split("://", 1)[1]
    creds, host_part = without_scheme.split("@", 1)
    user, password = creds.split(":", 1)
    host_port, dbname = host_part.split("/", 1)
    host, port = host_port.split(":") if ":" in host_port else (host_port, "3306")
    return {"user": user, "password": password, "host": host, "port": int(port), "database": dbname}


def main() -> None:
    if not settings.DATABASE_URL.startswith("mysql"):
        print("DATABASE_URL no es MySQL (probablemente SQLite de pruebas) — se omite la espera.")
        return

    conn_params = parse_mysql_url(settings.DATABASE_URL)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            connection = pymysql.connect(**conn_params, connect_timeout=3)
            connection.close()
            print("MySQL está listo.")
            return
        except Exception as exc:  # noqa: BLE001 — cualquier fallo de conexion cuenta como "todavia no"
            print(f"Esperando a MySQL... intento {attempt}/{MAX_ATTEMPTS} ({exc.__class__.__name__})")
            time.sleep(WAIT_SECONDS)

    print("MySQL no respondió a tiempo. Verifica que 'docker compose up -d' esté corriendo.")
    sys.exit(1)


if __name__ == "__main__":
    main()

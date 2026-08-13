"""
Genera .env a partir de .env.example, rellenando SECRET_KEY con un valor
aleatorio seguro. Se ejecuta una sola vez (si .env ya existe, no lo toca,
para no pisar configuracion que ya hayas personalizado).
"""
import secrets
from pathlib import Path

root = Path(__file__).resolve().parent.parent
env_path = root / ".env"
example_path = root / ".env.example"

if env_path.exists():
    print(".env ya existe, no se modifica.")
else:
    content = example_path.read_text(encoding="utf-8")
    random_secret = secrets.token_urlsafe(48)
    content = content.replace(
        "SECRET_KEY=cambia-esto-por-una-clave-larga-y-aleatoria",
        f"SECRET_KEY={random_secret}",
    )
    env_path.write_text(content, encoding="utf-8")
    print(".env creado con una SECRET_KEY generada automáticamente.")

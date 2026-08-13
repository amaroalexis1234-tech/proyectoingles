"""
Crea una cuenta de maestro directo en la base de datos. No hay auto-registro
publico de maestros (decision de producto) -- este script es el unico
mecanismo para crearlas mientras el numero de maestros sea pequeno.

Uso:
    python -m scripts.create_teacher --email maestro@upmh.edu --password ClaveSegura123 --name "Nombre Apellido"
"""
import argparse

from sqlmodel import Session, select

from app.core.database import engine
from app.core.security import hash_password
from app.modules.auth.models import User


def main() -> None:
    parser = argparse.ArgumentParser(description="Crea una cuenta de maestro.")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--name", required=True, dest="full_name")
    args = parser.parse_args()

    with Session(engine) as session:
        existing = session.exec(select(User).where(User.email == args.email)).first()
        if existing is not None:
            print(f"Ya existe una cuenta con el correo {args.email} (role={existing.role}).")
            return

        teacher = User(
            email=args.email,
            hashed_password=hash_password(args.password),
            full_name=args.full_name,
            role="teacher",
        )
        session.add(teacher)
        session.commit()
        print(f"Maestro creado: {args.email}")


if __name__ == "__main__":
    main()

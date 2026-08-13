# UPMH English Prep

Plataforma de preparación para el examen TOEFL ITP de la UPMH.

## Setup — un solo comando por parte

Requisitos previos: Python 3.11+, Node.js 20+, y Docker Desktop (para MySQL).

### 1. Base de datos

```
docker compose up -d
```

Esto levanta MySQL 8.4 con la base `umph_db` ya creada (usuario `umph_user`,
password `umph_password` — solo para desarrollo local, nunca usar en producción).

### 2. Backend

**Mac/Linux:**
```
cd umph-backend
./setup.sh
source venv/bin/activate
uvicorn app.main:app --reload
```

**Windows (cmd, no PowerShell — evita problemas de ExecutionPolicy):**
```
cd umph-backend
setup.bat
venv\Scripts\activate.bat
uvicorn app.main:app --reload
```

API disponible en `http://localhost:8000`, docs interactivas en `http://localhost:8000/docs`.

### 3. Frontend

**Mac/Linux:**
```
cd umph-frontend
./setup.sh
npm run dev
```

**Windows (cmd):**
```
cd umph-frontend
setup.bat
npm run dev
```

App disponible en `http://localhost:3000`.

## Qué hacen los scripts de setup

- Backend: crea el entorno virtual, instala dependencias, genera `.env` con una
  `SECRET_KEY` aleatoria segura, espera a que MySQL esté listo, y aplica las
  migraciones de Alembic.
- Frontend: instala dependencias y genera `.env.local`.

Ambos son seguros de correr más de una vez — si `.env`/`.env.local` ya existen,
no los sobreescriben.

## Estado del proyecto

Sprint 1 completado: arquitectura aprobada, estructura de carpetas, y módulo
de Auth completo (registro, login, refresh de sesión, recuperación de
contraseña backend) — frontend con Login y Registro conectados de verdad al
backend.

Próximo sprint: Dashboard.

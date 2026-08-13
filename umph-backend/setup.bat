@echo off
REM Deja el backend listo para correr: venv + dependencias + .env + migraciones.
REM Uso: setup.bat   (desde umph-backend\, doble clic o "cmd /c setup.bat")
REM Se usa .bat y no .ps1 a proposito: cmd no tiene restricciones de
REM ExecutionPolicy como PowerShell, asi que no requiere pasos extra.

echo == 1/5: Creando entorno virtual ==
if not exist venv (
    python -m venv venv
)

echo == 2/5: Activando entorno virtual ==
call venv\Scripts\activate.bat

echo == 3/5: Instalando dependencias ==
python -m pip install -q --upgrade pip
pip install -q -r requirements.txt
if errorlevel 1 goto :error

echo == 4/5: Generando .env (si no existe) ==
python scripts\init_env.py
if errorlevel 1 goto :error

echo == 5/5: Esperando MySQL y aplicando migraciones ==
python -m scripts.wait_for_db
if errorlevel 1 goto :error
alembic upgrade head
if errorlevel 1 goto :error

echo.
echo Listo. Para levantar el servidor:
echo   venv\Scripts\activate.bat
echo   uvicorn app.main:app --reload
goto :eof

:error
echo.
echo Algo fallo durante el setup. Revisa el mensaje de error de arriba.
exit /b 1

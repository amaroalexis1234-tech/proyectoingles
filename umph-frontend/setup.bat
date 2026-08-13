@echo off
REM Deja el frontend listo para correr: dependencias + .env.local

echo == 1/2: Instalando dependencias ==
call npm install
if errorlevel 1 goto :error

echo == 2/2: Generando .env.local (si no existe) ==
if not exist ".env.local" (
    copy .env.example .env.local >nul
    echo .env.local creado.
) else (
    echo .env.local ya existe, no se modifica.
)

echo.
echo Listo. Para levantar el servidor:
echo   npm run dev
goto :eof

:error
echo.
echo Algo fallo durante el setup. Revisa el mensaje de error de arriba.
exit /b 1

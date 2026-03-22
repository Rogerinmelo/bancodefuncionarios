@echo off
setlocal

echo Parando app...
docker compose down
if errorlevel 1 (
  echo.
  echo Falha ao parar. Verifique se o Docker Desktop esta aberto.
  pause
  exit /b 1
)

echo App parado com sucesso.
pause

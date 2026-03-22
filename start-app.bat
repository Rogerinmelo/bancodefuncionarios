@echo off
setlocal

echo Iniciando app completo (frontend + backend + banco + MinIO)...
docker compose up --build -d
if errorlevel 1 (
  echo.
  echo Falha ao iniciar. Verifique se o Docker Desktop esta aberto.
  pause
  exit /b 1
)

echo.
echo App pronto!
echo Frontend: http://localhost:5173
echo Backend docs: http://localhost:8000/docs
echo MinIO Console: http://localhost:9001  (usuario: minioadmin / senha: minioadmin)

echo.
echo Abrindo frontend no navegador...
start http://localhost:5173

pause

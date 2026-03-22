#!/usr/bin/env bash
set -e

echo "Subindo app completo (frontend + backend + banco + MinIO)..."
docker compose up --build -d

echo

echo "App pronto! Acesse:"
echo "- Frontend: http://localhost:5173"
echo "- Backend docs: http://localhost:8000/docs"
echo "- MinIO Console: http://localhost:9001 (minioadmin/minioadmin)"

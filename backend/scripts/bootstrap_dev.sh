#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "[1/6] Subindo PostgreSQL + MinIO..."
docker compose up -d

echo "[2/6] Criando virtualenv..."
python -m venv .venv

echo "[3/6] Instalando dependências..."
. .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

echo "[4/6] Configurando .env (se não existir)..."
cp -n .env.example .env || true

echo "[5/6] Aplicando migrações..."
alembic upgrade head

echo "[6/6] Ambiente pronto. Para iniciar API:"
echo "source .venv/bin/activate && uvicorn app.main:app --reload"

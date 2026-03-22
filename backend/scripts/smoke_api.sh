#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"

if ! command -v curl >/dev/null 2>&1; then
  echo "curl não encontrado"
  exit 1
fi

echo "[smoke] Healthcheck..."
curl -fsS "$BASE_URL/health" >/dev/null

echo "[smoke] Register company..."
COMPANY_RESPONSE=$(curl -fsS -X POST "$BASE_URL/api/v1/auth/register-company" \
  -H "Content-Type: application/json" \
  -d '{"name":"Empresa Smoke"}')

COMPANY_ID=$(python - <<'PY'
import json,sys
print(json.loads(sys.stdin.read())["id"])
PY
<<<"$COMPANY_RESPONSE")

echo "[smoke] Register user..."
curl -fsS -X POST "$BASE_URL/api/v1/auth/register-user" \
  -H "Content-Type: application/json" \
  -d "{\"company_id\":\"$COMPANY_ID\",\"name\":\"Admin Smoke\",\"email\":\"smoke@empresa.com\",\"password\":\"senha123\",\"role\":\"admin\"}" >/dev/null

echo "[smoke] Login..."
LOGIN_RESPONSE=$(curl -fsS -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"company_id\":\"$COMPANY_ID\",\"email\":\"smoke@empresa.com\",\"password\":\"senha123\"}")

ACCESS_TOKEN=$(python - <<'PY'
import json,sys
print(json.loads(sys.stdin.read())["access_token"])
PY
<<<"$LOGIN_RESPONSE")

echo "[smoke] Create employee..."
curl -fsS -X POST "$BASE_URL/api/v1/employees" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Funcionario Smoke"}' >/dev/null

echo "[smoke] OK"

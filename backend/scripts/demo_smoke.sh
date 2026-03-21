#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"

COMPANY_ID=$(curl -s -X POST "$BASE_URL/api/v1/auth/register-company" \
  -H "Content-Type: application/json" \
  -d '{"name":"Empresa Demo"}' | python -c 'import sys,json; print(json.load(sys.stdin)["id"])')

echo "company_id=$COMPANY_ID"

curl -s -X POST "$BASE_URL/api/v1/auth/register-user" \
  -H "Content-Type: application/json" \
  -d "{\"company_id\":\"$COMPANY_ID\",\"name\":\"Admin Demo\",\"email\":\"admin@demo.com\",\"password\":\"senha123\",\"role\":\"admin\"}" >/dev/null

ACCESS_TOKEN=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"company_id\":\"$COMPANY_ID\",\"email\":\"admin@demo.com\",\"password\":\"senha123\"}" | python -c 'import sys,json; print(json.load(sys.stdin)["access_token"])')

echo "token obtido"

EMPLOYEE_ID=$(curl -s -X POST "$BASE_URL/api/v1/employees" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Funcionario Demo"}' | python -c 'import sys,json; print(json.load(sys.stdin)["id"])')

SKILL_ID=$(curl -s -X POST "$BASE_URL/api/v1/skills" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"NR10"}' | python -c 'import sys,json; print(json.load(sys.stdin)["id"])')

curl -s -X POST "$BASE_URL/api/v1/employees/$EMPLOYEE_ID/skills" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"skill_id\":\"$SKILL_ID\",\"proficiency_level\":\"avancado\",\"years_experience\":5}" >/dev/null

DEMAND_ID=$(curl -s -X POST "$BASE_URL/api/v1/demands" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Licitação Demo","type":"licitacao","status":"aberta"}' | python -c 'import sys,json; print(json.load(sys.stdin)["id"])')

curl -s -X POST "$BASE_URL/api/v1/demands/$DEMAND_ID/skills" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"skill_id\":\"$SKILL_ID\",\"weight\":2,\"required\":true}" >/dev/null

echo "--- suggest-team ---"
curl -s -X POST "$BASE_URL/api/v1/demands/$DEMAND_ID/suggest-team" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | python -m json.tool

echo "--- build-task-force ---"
curl -s -X POST "$BASE_URL/api/v1/demands/$DEMAND_ID/build-task-force" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | python -m json.tool

echo "Smoke test finalizado com sucesso"

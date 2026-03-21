# API v1 — primeiros endpoints recomendados

## Auth

- `POST /api/v1/auth/register-company`
- `POST /api/v1/auth/register-user`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `GET /api/v1/auth/me`

## Funcionários

- `POST /api/v1/employees`
- `GET /api/v1/employees`
- `GET /api/v1/employees/{employee_id}`
- `PATCH /api/v1/employees/{employee_id}`
- `DELETE /api/v1/employees/{employee_id}` (soft delete / inativar)

## Habilidades

- `POST /api/v1/skills`
- `GET /api/v1/skills`
- `PATCH /api/v1/skills/{skill_id}`
- `DELETE /api/v1/skills/{skill_id}`

## Vínculo Funcionário ↔ Habilidade

- `POST /api/v1/employees/{employee_id}/skills`
- `PATCH /api/v1/employees/{employee_id}/skills/{skill_id}`
- `DELETE /api/v1/employees/{employee_id}/skills/{skill_id}`

## Payload base do vínculo de habilidade

```json
{
  "skill_id": "uuid",
  "proficiency_level": "intermediario",
  "years_experience": 3.5,
  "evidence_notes": "Atuou em instalações prediais por 3 anos"
}
```

## Convenções

- Todas as respostas com paginação para listas.
- Todos os endpoints protegidos (exceto login/registro).
- Filtro obrigatório por `company_id` extraído do token JWT.

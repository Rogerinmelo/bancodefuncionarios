# Backend (FastAPI)

## Como executar localmente

1. Suba o PostgreSQL:

```bash
docker compose up -d
```

2. Crie e ative um ambiente virtual e instale dependências:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

3. Copie as variáveis de ambiente:

```bash
cp .env.example .env
```

4. Rode as migrações Alembic:

```bash
alembic upgrade head
```

5. Rode a API:

```bash
uvicorn app.main:app --reload
```

## Testes

```bash
pytest
```

## Endpoints iniciais

- `GET /health`
- `POST /api/v1/auth/register-company`
- `POST /api/v1/auth/register-user`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `GET /api/v1/auth/me`
- CRUD básico de funcionários, habilidades, serviços e vínculo funcionário↔habilidade.


## Próximos passos sugeridos

1. Implementar módulo de demandas/licitações (modelo + migração + CRUD).
2. Adicionar requisitos técnicos por demanda (`demand_skill_requirements`).
3. Implementar histórico de serviços do funcionário com upload de fotos (S3/MinIO).
4. Criar endpoint de sugestão de equipe (`suggest-team`) com score inicial.
5. Configurar CI para rodar `pytest` e `alembic upgrade head` automaticamente.

- `POST /api/v1/demands`
- `POST /api/v1/demands/{demand_id}/skills`
- `POST /api/v1/demands/{demand_id}/suggest-team`
- `POST /api/v1/employees/{employee_id}/history`
- `POST /api/v1/employees/{employee_id}/history/{history_id}/photos`
- `POST /api/v1/demands/{demand_id}/build-task-force`
- `GET /api/v1/demands/{demand_id}/suggestions/latest`

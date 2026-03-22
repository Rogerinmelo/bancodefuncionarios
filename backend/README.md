# Backend (FastAPI)

## Como rodar o app (passo a passo)

1. Suba infraestrutura local (PostgreSQL + MinIO):

```bash
docker compose up -d
```

2. Crie e ative ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Instale dependências:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

4. Configure variáveis:

```bash
cp .env.example .env
```


5. Rode as migrações:

```bash
alembic upgrade head
```

6. Inicie a API:

```bash
uvicorn app.main:app --reload
```

7. Acesse:
- API docs (Swagger): `http://127.0.0.1:8000/docs`
- Healthcheck: `http://127.0.0.1:8000/health`
- MinIO Console: `http://127.0.0.1:9001` (user/pass: `minioadmin`)

## Fluxo rápido para testar no Postman/Insomnia

1. `POST /api/v1/auth/register-company`
2. `POST /api/v1/auth/register-user`
3. `POST /api/v1/auth/login`
4. Use `Authorization: Bearer <access_token>` nas rotas protegidas.

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

1. Criar endpoint de versão específica de snapshot de sugestão (`/demands/{demand_id}/suggestions/{version}`).
2. Adicionar explicabilidade do score por funcionário (quais skills e pesos influenciaram no resultado).
3. Implementar gerenciamento de membros da força-tarefa (editar/remover membro e papéis no time).
4. Aplicar RBAC completo em todos os módulos legados (employees, skills, services) com matriz de permissões.
5. Publicar documentação OpenAPI por perfil e exemplos prontos para integração frontend.


## Atalhos de execução

- `make up` → sobe Postgres + MinIO
- `make install` → cria venv e instala dependências
- `make env` → cria `.env` a partir de `.env.example`
- `make migrate` → aplica migrações
- `make run` → inicia API
- `make test` → roda testes
- `make smoke` → smoke test básico da API

Scripts:
- `scripts/bootstrap_dev.sh` (setup completo de ambiente)
- `scripts/smoke_api.sh` (validação rápida de fluxo auth + employee)

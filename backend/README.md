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

1. Criar endpoint de versão específica de snapshot de sugestão (`/demands/{demand_id}/suggestions/{version}`).
2. Adicionar explicabilidade do score por funcionário (quais skills e pesos influenciaram no resultado).
3. Implementar gerenciamento de membros da força-tarefa (editar/remover membro e papéis no time).
4. Aplicar RBAC completo em todos os módulos legados (employees, skills, services) com matriz de permissões.
5. Publicar documentação OpenAPI por perfil e exemplos prontos para integração frontend.

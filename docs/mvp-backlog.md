# Próximo passo (prático): Sprint 1

Objetivo da Sprint 1: colocar o sistema no ar localmente com autenticação e os dois primeiros módulos de negócio.

## Entregas da sprint

1. **Infra base do projeto**
   - Estruturar repositório em `frontend/` e `backend/`
   - Configurar variáveis de ambiente (`.env.example`)
   - Subir PostgreSQL local com Docker Compose

2. **Autenticação multiempresa**
   - Cadastro de `company`
   - Cadastro e login de usuário (JWT + refresh token)
   - Middleware para resolver `company_id` do usuário autenticado

3. **Módulo Funcionários (CRUD)**
   - Criar, listar, detalhar, atualizar e inativar funcionário
   - Garantir isolamento por empresa (`company_id`)

4. **Módulo Habilidades (CRUD + vínculo)**
   - CRUD de habilidades por empresa
   - Vincular habilidade ao funcionário com nível e anos de experiência

5. **Regras de qualidade mínimas**
   - Migrações versionadas
   - Testes de API para autenticação e permissões multiempresa
   - Seed inicial para ambiente local

## Critérios de pronto (DoD)

- API funcional para autenticação, funcionários e habilidades.
- Banco com migrações aplicáveis em ambiente limpo.
- Usuário da Empresa A não visualiza dados da Empresa B.
- Coleção de requests (Insomnia/Postman) ou OpenAPI validada.

## Ordem de execução sugerida (sem travar)

1. Banco + migrações + modelos
2. Auth (login/refresh)
3. CRUD Funcionários
4. CRUD Habilidades
5. Vínculo funcionário-habilidade
6. Testes de isolamento multiempresa

## Riscos e mitigação

- **Risco:** complexidade de multi-tenant vazar dados.
  - **Mitigação:** filtrar por `company_id` em todas as queries e testes de contrato.
- **Risco:** escopo crescer cedo demais.
  - **Mitigação:** travar Sprint 1 somente em auth + funcionários + habilidades.

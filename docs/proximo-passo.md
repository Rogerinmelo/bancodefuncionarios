# Próximo passo recomendado (após Auth + Funcionários + Habilidades)

## Objetivo
Entrar na **Sprint 2**: histórico prático + serviços + demandas/licitações + sugestão inicial de equipe.

## Entregas da Sprint 2 (ordem sugerida)

1. **Módulo Serviços (CRUD)**
   - Endpoints:
     - `POST /api/v1/services`
     - `GET /api/v1/services`
     - `PATCH /api/v1/services/{service_id}`
     - `DELETE /api/v1/services/{service_id}`
   - Regras:
     - isolamento por `company_id`
     - nome único por empresa

2. **Módulo Demandas/Licitações (CRUD)**
   - Endpoints:
     - `POST /api/v1/demands`
     - `GET /api/v1/demands`
     - `GET /api/v1/demands/{demand_id}`
     - `PATCH /api/v1/demands/{demand_id}`
   - Regras:
     - status da demanda (`aberta`, `em_analise`, `em_execucao`, `encerrada`)
     - vínculo opcional com serviço

3. **Requisitos técnicos da demanda**
   - Endpoints:
     - `POST /api/v1/demands/{demand_id}/skills`
     - `DELETE /api/v1/demands/{demand_id}/skills/{skill_id}`
   - Regras:
     - peso por habilidade (`weight`)
     - flag obrigatória vs desejável

4. **Histórico prático de funcionário (comentários + fotos)**
   - Endpoints:
     - `POST /api/v1/employees/{employee_id}/history`
     - `GET /api/v1/employees/{employee_id}/history`
     - `POST /api/v1/employees/{employee_id}/history/{history_id}/photos`
   - Regras:
     - salvar metadados da foto no banco
     - arquivo em storage S3 compatível (MinIO local)

5. **Sugestão inicial de equipe (matching v1)**
   - Endpoint:
     - `POST /api/v1/demands/{demand_id}/suggest-team`
   - Estratégia inicial:
     - score por aderência de habilidades obrigatórias
     - bônus por anos de experiência
     - retornar ranking top N

## Critérios de pronto

- Alembic com novas migrações para serviços, demandas e histórico.
- Testes de integração cobrindo:
  - isolamento multi-tenant
  - regra de matching mínima
  - upload de foto (mock do storage)
- OpenAPI refletindo todos os novos endpoints.

## Dica prática para execução

Começar por **Serviços + Demandas** (sem fotos), depois adicionar histórico/fotos e por fim o matching.

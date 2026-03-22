# BNC de Funcionários

Aplicação web para **gerenciamento de funcionários**, com foco em:
- cadastro completo de colaboradores,
- histórico técnico e educacional,
- montagem de força-tarefa,
- apoio à seleção de equipe para serviços e licitações.

## Visão geral do produto

O sistema será **multiempresa (multi-tenant)**, com autenticação e isolamento de dados por empresa.

### Módulos principais

1. **Funcionários**
   - dados pessoais (nome, CPF, telefone, endereço, data de nascimento, etc.)
   - status (ativo/inativo)
   - observações gerais

2. **Habilidades**
   - catálogo de habilidades por empresa
   - nível de proficiência por funcionário (iniciante/intermediário/avançado)
   - tempo de experiência e evidências

3. **Cursos & Formações**
   - formação acadêmica
   - cursos livres e certificações
   - validade de certificados e anexos

4. **Serviços**
   - catálogo dos serviços executados pela empresa
   - habilidades recomendadas/requeridas por tipo de serviço

5. **Demandas / Licitações**
   - cadastro de oportunidades
   - requisitos técnicos (habilidades obrigatórias e desejáveis)
   - prazo, local, orçamento e criticidade

6. **Força-Tarefa**
   - criação de equipes para uma demanda
   - visão agregada das habilidades do time
   - identificação de gaps (habilidades faltantes)

7. **Histórico prático (Comentários + Fotos)**
   - registros de serviços executados por funcionário
   - comentários de desempenho
   - upload de fotos e evidências para referência futura


## Funcionalidades já integradas (status atual)

- **Autenticação multiempresa** com registro de empresa, usuário, login, refresh token e endpoint `/auth/me`.
- **Controle de acesso por perfil (RBAC inicial)**: operações críticas de demanda/histórico protegidas para `admin` e `gestor`, com leitura permitida a `viewer` onde aplicável.
- **Funcionários**: CRUD com inativação (soft delete) e isolamento por `company_id`.
- **Habilidades**: CRUD por empresa e vínculo funcionário↔habilidade com nível e experiência.
- **Serviços**: CRUD por empresa com unicidade de nome por tenant.
- **Demandas/Licitações**: CRUD, requisitos técnicos por demanda e remoção de requisitos.
- **Sugestão de equipe**: ranking por aderência de skills obrigatórias + experiência, com persistência versionada de snapshots.
- **Força-tarefa**: endpoint para montar time multiusuário por demanda visando melhor cobertura de skills.
- **Histórico prático**: registro de atividades por funcionário, com upload de fotos para S3/MinIO.
- **Upload protegido**: validação de tipo/tamanho de arquivo e geração de URL assinada para acesso ao objeto.
- **Banco versionado** com Alembic e migrations encadeadas.
- **Testes de integração** para auth, isolamento multi-tenant, serviços, demandas, histórico, validações de upload e permissões por perfil.
- **CI** no GitHub Actions executando migração e testes automaticamente.

## Stack inicial (MVP)

- **Frontend:** React + Vite + TypeScript
- **Backend:** FastAPI (Python)
- **Banco de dados:** PostgreSQL
- **Autenticação:** JWT com refresh token
- **Armazenamento de arquivos (fotos):** S3 compatível (ex.: MinIO em desenvolvimento)

## Diretrizes de arquitetura

- Multi-tenant por `company_id` em todas as entidades de negócio.
- Controle de acesso por perfil (ex.: admin da empresa, gestor, visualizador).
- API REST com versionamento (`/api/v1`).
- Auditoria básica (`created_at`, `updated_at`, `created_by`).

## Roadmap sugerido

### Fase 1 — Fundação
- autenticação e cadastro de empresas/usuários
- CRUD de funcionários
- CRUD de habilidades
- vínculo funcionário ↔ habilidade

### Fase 2 — Qualificação e histórico
- cursos, formações e certificações
- histórico de serviços com comentários/fotos

### Fase 3 — Inteligência operacional
- cadastro de demandas/licitações
- sugestão automática de melhores funcionários (score)
- montagem de força-tarefa com visão consolidada de competências

### Fase 4 — Deploy
- estabilização e testes
- deploy em ambiente online
- monitoramento, backup e governança de dados

## Critérios para sugestão automática (matching)

Exemplo de score:

```text
score_total =
  (peso_habilidades * aderencia_habilidades) +
  (peso_experiencia * experiencia_servicos_similares) +
  (peso_certificacoes * certificacoes_validas) +
  (peso_disponibilidade * disponibilidade_no_periodo)
```

Com isso o sistema pode:
- ranquear funcionários para cada demanda,
- sugerir combinações de equipe,
- indicar quais habilidades estão faltando no time atual.

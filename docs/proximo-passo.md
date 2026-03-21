# Próximo passo recomendado (após módulo de Demandas/Histórico já integrado)

## Objetivo
Consolidar governança e observabilidade da decisão de alocação de equipes.

## Entregas sugeridas (ordem)

1. **Snapshots avançados de sugestão**
   - endpoint por versão (`GET /api/v1/demands/{demand_id}/suggestions/{version}`)
   - comparação entre versões (delta de score)

2. **Explicabilidade do score**
   - detalhar por funcionário: skills atendidas, pesos aplicados e bônus por experiência
   - armazenar justificativa no snapshot

3. **Gestão completa de Força-Tarefa**
   - listar força-tarefa por demanda
   - editar papel/membro
   - remover membro e recalcular cobertura

4. **RBAC completo**
   - matriz de permissões por módulo (admin/gestor/viewer)
   - testes de autorização para endpoints legados

5. **Observabilidade e auditoria**
   - logs estruturados por request
   - trilha de auditoria para mudanças críticas

## Critérios de pronto

- Documentação OpenAPI atualizada com exemplos por perfil.
- Testes cobrindo cenários positivos e negativos de RBAC.
- Snapshot com explicação detalhada de score consultável por API.

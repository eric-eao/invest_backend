# 📄 Log de Implementações

## 🟢 Implementações Realizadas

### [2025-06-29]
- Estrutura inicial de rotas do `categories` montada  
- Separação do `get_db` para `app/core/db/session.py`  
- Handlers do `categories` criados para isolar regras de negócio  
- Container validado com Docker rodando corretamente  
- Primeiro commit e push para o GitHub  
- Estrutura inicial do projeto em FastAPI montada com padrão de pastas definido  
- Docker Compose configurado para PostgreSQL (`investcontrol`)  
- Ambiente Python virtual (.venv) configurado  
- Alembic inicializado e sincronizado sem pendências  
- Primeira migration gerada e aplicada com sucesso para a tabela `categories`  
- Banco de dados limpo e revisado, sem tabelas residuais  
- Conexão validada manualmente com `psql`  
- Criação dos handlers para operações de categoria (`create`, `update`, `delete`, `list`)  
- Rotas completas de categoria (`routes/categories.py`)  

### [2025-06-30]
- Campo `module` fixado no handler como valor hardcoded  
- Ajuste do schema `CategoryUpdate` para permitir updates parciais corretamente (`Optional` com `= None`)  
- Ajuste do `CategoryBase` e `CategoryOut` para OpenAPI compatível com Pydantic v2  
- Testes automatizados do CRUD de categorias passando integralmente  
- Correções de permissões e grants no banco de produção  
- Swagger revisado e melhorado com descrições e exemplos corretos  
- Configuração do PATCH para updates parciais sem exigir todos os campos  
- Migration e criação da tabela `control_benchmarks` concluída  
- Implementação do CRUD completo de benchmarks  
- Handlers separados para benchmarks (`core/benchmarks/handlers`)  
- Rotas organizadas em `routes/admin/benchmarks.py` sem prefixo fixo  
- Prefixo do benchmarks controlado diretamente no `main.py`

### [2025-07-01]
- Implementado CRUD completo do `private_credit_assets`  
- Inclusão do validador de regras de rentabilidade centralizado (`asset_validator.py`)  
- Rotas de asset disponíveis em `/private-credit/assets`  
- Integração ao category_id com `private_credit_categories`  
- Validado funcionamento de updates parciais respeitando regras de prefixado/pós-fixado  
- Migration revisada e aplicada sem pendências  
- Criação da tabela `positions` para consolidar lotes FIFO de ativos  
- Implementação do service genérico `process_positions_service`  
- Ajustes nos handlers de movimento (`create`, `update`, `delete`) para:  
  - marcar movimento como `PENDING` ao editar  
  - reprocessar apenas os movimentos pendentes  
  - deletar e reconstruir apenas lotes relacionados ao asset do movimento excluído  
- Ajuste de status de movimentos para `CONFIRMED` ao processar FIFO  
- Integração completa entre movimentações, FIFO e positions  
- Revisão e sincronização do sync dos benchmarks (`snapshot_sync_service`) incluindo a conversão de taxas mensais para diárias (IPCA)  
- Limpeza do código legado de acumulados (`snapshot_calculate_accumulated_service` removido)  
- Correção do fluxo de recalculo de PU (marcação a mercado) futura, já preparada na modelagem

### [2025-07-06]
- Revisão completa do fluxo de positions e movimentos com controle de status (PENDING / CONFIRMED)  
- Ajustado `process_positions_service` para reprocessar apenas movimentos pendentes, respeitando FIFO e preservando históricos confirmados  
- Ajustado `delete_movement` para marcar **apenas os movimentos do mesmo asset** como pendentes antes de recalcular posições  
- Atualizado fluxo de benchmark para conversão de taxas mensais (IPCA) para diárias já no sync, eliminando necessidade de recalcular acumulados posteriormente  
- Removido service de acumulados legado (`snapshot_calculate_accumulated_service`)  
- Garantido consistência do fluxo de update de movimentos: ao atualizar, o status do movimento passa a ser obrigatoriamente PENDING  
- Consolidado o fluxo de recalculo das posições em todas as operações (create, update, delete)  
- Atualizado a documentação de processos e regras de FIFO (explicando também o uso de positions como base para marcação a mercado futura)  
- Testes manuais validados em endpoints de movimentações, incluindo fluxo de FIFO parcial (lote aberto e fechado)  
- Alinhamento de nomenclatura para positions globais, removendo prefixo `private_credit_` para permitir reuso do service em outros módulos  
- Ajustado handlers para refletir a estratégia de deletar apenas lotes afetados por movimentos pendentes, sem comprometer dados confirmados  
- Atualização do commit e histórico de projeto para refletir toda a refatoração de positions e melhorias no módulo de movimentações

### [2025-07-06]
- Planejar a modelagem e implementação do módulo de marcação a mercado (PU, rentabilidade lote a lote)  

---

## 🔮 Próximas Implementações

- Avaliar o erro na inclusão do movement junto com a criação do asset, erro de module_id

- Refatoração e organização dos testes em arquivos separados por contexto  
- Adição de testes negativos e casos de erro (404, 409, etc) para cobertura completa  
- Padronização dos nomes e mensagens de erro no handler  
- Criar testes unitários e de integração para o CRUD de `private_credit_assets`, incluindo casos negativos de validação  
- Montar seeds de dados de ativos de exemplo para ambiente de testes/admin  
- Avaliar expandir a resposta do asset para incluir dados da categoria aninhada  
- Estruturar logs/auditoria para rastrear alterações nos ativos (quem alterou, quando, e qual campo)
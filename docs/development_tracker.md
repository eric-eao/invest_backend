## 🟢 Implementações Realizadas

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
- Campo `module` fixado no handler como valor hardcoded  
- Ajuste do schema `CategoryUpdate` para permitir updates parciais corretamente (`Optional` com `= None`)  
- Ajuste do `CategoryBase` e `CategoryOut` para OpenAPI compatível com Pydantic v2  
- Testes automatizados do CRUD de categorias passando integralmente  
- Correções de permissões e grants no banco de produção  
- Swagger revisado e melhorado com descrições e exemplos corretos  
- Configuração do PATCH para updates parciais sem exigir todos os campos  

---

## 🔮 Próximas Implementações

- Refatoração e organização dos testes em arquivos separados por contexto  
- Adição de testes negativos e casos de erro (404, 409, etc) para cobertura completa  
- Padronização dos nomes e mensagens de erro no handler  
- Continuação da documentação OpenAPI dos endpoints de categoria  
- Início do módulo de **movements** (CRUD de movimentações financeiras)

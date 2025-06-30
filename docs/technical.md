# 📊 Investments Project — Technical Documentation

## 🖥️ Ambiente de Desenvolvimento

- Sistema Host: Windows
- Subsistema: WSL2 (Windows Subsystem for Linux)
- Distro recomendada: Ubuntu 22.04 LTS
- Docker Desktop: executando integrado ao WSL2
- Editor recomendado: VS Code com extensão Remote - WSL
- Banco de dados Postgres: containerizado no ambiente Linux
- Portas expostas:
  - 5432 (Postgres)
  - 8000 (FastAPI)

## 📌 Context

- **Objetivo**: Construir sistema modular para controle de investimentos, incluindo cadastro de ativos, controle de movimentações e geração de relatórios de rentabilidade.
- **Linguagem backend**: Python
- **Framework**: FastAPI
- **Banco de dados**: PostgreSQL (rodando via Docker)
- **Módulos iniciais**:
  - Private Credit (renda fixa privada)
  - Bonds (renda fixa pública)
  - Equities (ações e ETFs, futuro)
- **Containerização**: docker-compose
- **Versão inicial**: sem versionamento de API

---

## 🗂️ Banco de Dados

- **Database padrão**: `investments_db`
- **User padrão**: `investments_user`
- **Senha padrão**: `investments_pass`
- **Extensões ativas**:
  - `uuid-ossp`: para geração de UUIDs confiáveis
  - `pg_trgm`: para buscas textuais rápidas e fuzzy
  - `pg_stat_statements`: monitoramento de performance de queries

### Estrutura inicial de tabelas

#### categories

| Campo              | Tipo      | Descrição                                      |
|--------------------|-----------|------------------------------------------------|
| id                 | integer   | identificador único (PK)                       |
| name               | string    | nome da categoria                              |
| description        | string    | descrição longa                                |
| allocation_planned | float     | percentual planejado de alocação (0–100%)      |
| currency           | string    | moeda da categoria (ex.: BRL, USD, EUR)        |
| active             | boolean   | status de ativação                             |
| module             | string    | módulo associado (private_credit, bonds, etc.) |
| created_at         | timestamp | data de criação                                |
| updated_at         | timestamp | data de atualização                            |

> **Constraints**
> - UNIQUE(name, module)
> - currency como ENUM fixo (BRL, USD, EUR)
> - allocation_planned validado entre 0–100

---

#### control_benchmarks

| Campo        | Tipo      | Descrição                                                       |
|--------------|-----------|-----------------------------------------------------------------|
| id           | integer   | identificador único                                             |
| name         | string    | nome do benchmark                                               |
| description  | string    | descrição completa                                              |
| active       | boolean   | status de sincronização                                         |
| sync_status  | string    | status atual do sincronismo (OK, FAILED, IN_PROGRESS)           |
| sync_from    | date      | data inicial sincronizada                                       |
| sync_to      | date      | data final sincronizada                                         |
| created_at   | timestamp | data de criação                                                 |
| updated_at   | timestamp | data de atualização                                             |

---

#### control_portfolio_dates

| Campo             | Tipo      | Descrição                                                    |
|-------------------|-----------|--------------------------------------------------------------|
| id                | integer   | identificador único                                          |
| module_id         | integer   | referência ao control_modules                                |
| first_investment  | date      | data do investimento mais antigo registrado na carteira      |
| last_investment   | date      | data do investimento mais recente registrado na carteira     |
| active            | boolean   | status de controle                                           |
| updated_at        | timestamp | data de atualização                                          |

---

#### control_modules

| Campo          | Tipo      | Descrição                                                      |
|----------------|-----------|----------------------------------------------------------------|
| id             | integer   | identificador único                                            |
| name           | string    | nome do módulo (ex.: private_credit)                           |
| description    | string    | descrição completa                                             |
| active         | boolean   | status de ativação                                             |
| sync_status    | string    | status de sincronização geral                                  |
| last_sync_at   | timestamp | data/hora da última sincronização concluída                    |
| created_at     | timestamp | data de criação                                                |
| updated_at     | timestamp | data de atualização                                            |

---

## ⚙️ Backend Stack

- **FastAPI**: framework principal
- **SQLAlchemy**: ORM
- **Alembic**: migrations
- **Pydantic**: schemas de validação
- **Uvicorn**: servidor ASGI
- **pytest**: framework de testes
- **python-decouple**: variáveis de ambiente (.env)

> **Observação**  
> - loguru, httpx, tenacity, fastapi-utils **não** serão instalados inicialmente, apenas futuramente se houver necessidade.

---

## 🛠️ Infraestrutura Docker

- Postgres 16 rodando em container
- FastAPI rodando em container separado
- Rede Docker chamada `investments_net`
- Volume persistente para dados Postgres
- Porta padrão Postgres 5432
- Porta padrão FastAPI 8000

---

## 🚦 Padrões de API

- **Versionamento**: sem prefixo de versão no momento
- **Autenticação**: não implementada inicialmente
- **Rotas**: sempre plural
  - `/categories`
  - `/assets`
  - `/movements`
- **Auditoria**: será avaliada posteriormente
- **Deploy**: ambiente local no início; estratégia de nuvem será definida futuramente

---

## 🔄 Handlers

- **movements handler**
  - responsável central por todo CRUD de movimentações
  - fará atualização automática de tabelas de controle (ex.: control_portfolio_dates)
  - disparará eventos de log/auditoria se necessário
- **categories handler**
  - CRUD completo
  - validará allocation_planned e campos obrigatórios
  - padronização de erros e status codes

---

## Banco de Dados

- Reinicializado o volume Docker (`pgdata`) para garantir ambiente limpo.
- Reset completo do banco `investcontrol`, recriado sem tabelas herdadas.
- Alembic reiniciado (pasta `versions` limpa) e gerado novo revision base para a tabela `categories`.
- Migrations aplicadas do zero, ambiente migrado sem inconsistências.

---

## Alembic

- Configurado para PostgreSQL
- Realizado primeiro revision de `categories` sem conflitos anteriores
- Confirmado `alembic upgrade head` executado sem erros

---

## Handlers e Rotas

- Handlers de categoria (`create`, `update`, `delete`, `list`) completos
- Rotas FastAPI de categoria integradas e testadas localmente

---

## 📎 Observações Finais

- Documentação deve ser mantida sempre atualizada conforme mudanças de modelo de dados.  
- Padrão de nomes:
  - snake_case no banco
  - camelCase opcional no Pydantic (se desejar facilitar frontend)
- Estrutura modular para crescimento futuro
- Esta documentação serve de **guia fixo** para qualquer retomada do projeto.

---

> **IMPORTANTE**  
> Qualquer dúvida futura sobre padrões, rotas ou regras, este documento é a *fonte de verdade*.  
> Todas as decisões devem seguir o que está aqui, salvo mudança **explícita** em alinhamento futuro.


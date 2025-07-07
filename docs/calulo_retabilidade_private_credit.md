# 📄 Blueprint - Controle de Rentabilidade Private Credit

## 1️⃣ Objetivo

Construir um mecanismo de **marcação a mercado** (*mark-to-market*) para ativos de crédito privado, calculando:

- `current_unit_price`
- `last_valuation_date`
- `profitability_percent`
- `profitability_amount`
- `last_valuation_date`


de forma **fidedigna**, considerando:

- múltiplos aportes
- resgates parciais
- indexadores (CDI, IPCA, prefixado)
- movimentos ao longo do tempo

---

## 9️⃣ Definição do campo `last_valuation_date`

O campo `last_valuation_date` do asset representa a **última data de avaliação confiável** do preço do ativo, considerando a informação de benchmark disponível.  

- Para ativos indexados ao **CDI**:
  - utilizar a data de hoje, pois a taxa diária está sempre atualizada.

- Para ativos indexados ao **IPCA**:
  - utilizar a **última data** onde houve taxa diária gerada no `snapshot_benchmarks`,
    normalmente correspondente ao último pregão do mês em que a taxa mensal foi publicada e convertida.
  - Exemplo: se o IPCA de maio foi a última taxa conhecida e foi distribuído até o dia 29/05/2025,
    então o `last_valuation_date` deve ser **29/05/2025**.

Dessa forma, garante-se ao investidor transparência sobre a defasagem de dados do ativo
e a rastreabilidade completa do mark-to-market.

---

## 2️⃣ Premissas do cálculo

- O ativo parte de um PU inicial de referência (ex: 1000)
- Cada **aplicação** cria um “lote” de cotas, com data própria
- Cada **resgate** retira cotas de forma **FIFO** (primeiro que entrou, primeiro que sai)
- O saldo atual deve ser consolidado dos lotes sobreviventes, ponderando quantidade e preço médio

---

## 3️⃣ Fontes de dados

- **Tabela `private_credit_assets`**
  - cadastro do ativo
  - guarda sumário: quantidade total, custo total, preço médio
  - campos a calcular:
    - current_unit_price
    - last_valuation_date
    - profitability_percent
    - profitability_amount

- **Tabela `movements`**
  - todas as movimentações (DEPOSIT, FULL_REDEMPTION, PARTIAL_REDEMPTION)
  - campos principais:
    - asset_id
    - date
    - quantity
    - unit_price
    - type

- **Tabela `control_benchmarks`**
  - benchmark de indexação (ex. CDI, IPCA)
  - identificamos o benchmark_id

- **Tabela `snapshot_benchmarks`**
  - taxas diárias (ou mensais no caso do IPCA) do benchmark
  - benchmark_id + data + taxa

---

## 4️⃣ Regras de cálculo

### Prefixado
- indexer = null
- taxa fixa anual (`fixed_rate`)
- projeção do PU:
PU = 1000 * (1 + fixed_rate)^(dias_corridos/252)

---

### Pós-fixado CDI
- indexer = CDI
- percentual sobre CDI (`index_percent`)
- fator composto:
PU = 1000 * PRODUCT(1 + CDI_diario/100 * index_percent/100)

---

### Pós-fixado IPCA + spread
- indexer = IPCA
- spread = taxa adicional anual
- fator composto:
PU = 1000 * PRODUCT(1 + IPCA_diario) * (1 + spread/252)^dias
> observação: o IPCA diário virá convertido da taxa mensal

---

## 5️⃣ Processamento esperado

1. **varrer as movimentações do ativo**
 - classificar DEPOSIT, FULL_REDEMPTION, PARTIAL_REDEMPTION
 - organizar **lotes**:
   - data de início
   - quantidade
   - preço unitário

2. **FIFO nos resgates**
 - ao processar um resgate, consumir a quantidade do primeiro lote em aberto
 - se acabar a quantidade do lote, remove o lote
 - passa para o próximo
 - ajusta a quantidade remanescente

3. **após processar todos os movimentos**
 - restarão apenas os lotes vivos
 - para cada lote vivo:
   - calcular PU do indexador desde a data do aporte até a data atual
   - aplicar a rentabilidade composta
   - multiplicar pela quantidade viva do lote

4. **consolidar**
 - somar todos os lotes vivos ponderando quantidade
 - calcular:
   - `current_unit_price` (média ponderada atual dos lotes vivos)
   - `profitability_percent` (vs. preço médio de aquisição)
   - `profitability_amount` (ganho financeiro total do ativo)

5. **atualizar o asset**
 - campos:
   - current_unit_price
   - last_valuation_date
   - profitability_percent
   - profitability_amount

---

## 6️⃣ Desafios / pontos de atenção

- converter IPCA mensal → IPCA diário
- garantir consistência nos períodos (datas sem taxa → considerar taxa zero ou replicar última disponível)
- tratar resgates parciais corretamente
- manter FIFO estável e confiável
- prever valores de PU nos dias sem movimento (marcação intermediária)

---

## 7️⃣ Estrutura de código sugerida

- handlers
- `calculate_private_credit_handler.py`
- services
- `calculate_private_credit_service.py`
- `update_asset_position_service.py` (já existente)
- utils para lotes (opcional `lotes_utils.py`)

---

## 8️⃣ Resumo do fluxo

**Fluxo completo esperado:**

- handler → dispara cálculo
- service → processa ativos um a um
- reconstrói posição
- reconstrói lotes
- aplica marcação a mercado por indexador
- consolida
- salva
- ao final → retorna mensagem de sucesso + lista de ativos processados

---

## Próximos passos

Quando quiser, podemos atacar **passo 1 (lógica de lotes FIFO)** juntos.
Basta sinalizar.

---

## 9️⃣ Definição do campo `last_valuation_date`

O campo `last_valuation_date` do asset representa a **última data de avaliação confiável** do preço do ativo, considerando a informação de benchmark disponível.  

- Para ativos indexados ao **CDI**:
  - utilizar a data de hoje, pois a taxa diária está sempre atualizada.

- Para ativos indexados ao **IPCA**:
  - utilizar a **última data** onde houve taxa diária gerada no `snapshot_benchmarks`,
    normalmente correspondente ao último pregão do mês em que a taxa mensal foi publicada e convertida.
  - Exemplo: se o IPCA de maio foi a última taxa conhecida e foi distribuído até o dia 29/05/2025,
    então o `last_valuation_date` deve ser **29/05/2025**.

Dessa forma, garante-se ao investidor transparência sobre a defasagem de dados do ativo
e a rastreabilidade completa do mark-to-market.

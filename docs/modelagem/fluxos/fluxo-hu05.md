# Fluxo da Funcionalidade - HU05 (Resumo de Despesas por Categoria)

## Descrição

Este documento descreve o fluxo completo da funcionalidade de resumo de despesas por categoria, permitindo ao usuário visualizar a distribuição dos seus gastos, identificar as categorias com maior impacto financeiro e acompanhar os resultados por período.

## Responsável

Gabriel Lopes da Silva

## História de Usuário

Como usuário do sistema, quero visualizar o resumo de despesas por categoria, para entender onde estou gastando mais.

---

## Definição

A funcionalidade agrupa automaticamente todas as despesas cadastradas por categoria, calculando o valor total gasto em cada uma delas para o período selecionado.

As informações são utilizadas para alimentar os gráficos estatísticos do sistema e fornecer uma visão consolidada da distribuição dos gastos.

### Características

- Agrupamento automático das despesas por categoria
- Soma do valor total gasto em cada categoria
- Filtragem por mês e ano
- Integração com os gráficos financeiros
- Exibição das porcentagens de participação de cada categoria
- Atualização automática conforme novos lançamentos

---

## Regras de Negócio

- Apenas despesas do usuário autenticado devem ser consideradas.
- O sistema deve agrupar automaticamente as despesas por categoria.
- Deve ser apresentado o valor total gasto por categoria.
- O resumo deve considerar apenas o período selecionado.
- Alterações nas despesas devem atualizar automaticamente os valores apresentados.
- Categorias sem despesas no período não devem ser exibidas.

---

## Fluxo da Funcionalidade

### Seleção do período

1. Usuário acessa a tela de gráficos financeiros.
2. Sistema considera o mês e ano selecionados.
3. Caso nenhum período seja informado, utiliza o mês atual.

---

### Processamento

4. Sistema consulta todas as despesas do usuário no período.

5. As despesas são agrupadas por categoria.

6. Para cada categoria, o sistema calcula:

- Valor total gasto.
- Participação percentual no total das despesas.
- Cor personalizada da categoria.

---

### Exibição

7. Sistema apresenta:

- Resumo por categoria.
- Percentual correspondente.
- Gráfico de distribuição.
- Legenda das categorias.

---

### Atualização

8. Sempre que uma despesa for:

- cadastrada;
- editada;
- excluída;

o resumo é recalculado automaticamente.

---

## Critérios de Aceitação

**CA01 — Agrupamento**

Dado que existam despesas cadastradas

Quando o usuário acessar os gráficos

Então o sistema deve agrupar automaticamente os gastos por categoria.

---

**CA02 — Total por categoria**

Dado que existam despesas em uma categoria

Quando o resumo for gerado

Então deve ser apresentado o valor total gasto naquela categoria.

---

**CA03 — Filtragem por período**

Dado que o usuário selecione um mês

Quando visualizar o resumo

Então apenas as despesas daquele período devem ser consideradas.

---

**CA04 — Atualização automática**

Dado que uma despesa seja cadastrada, alterada ou excluída

Quando a operação for concluída

Então os valores do resumo devem ser atualizados automaticamente.

---

**CA05 — Percentuais**

Dado que existam despesas cadastradas

Quando o resumo for apresentado

Então o sistema deve calcular a participação percentual de cada categoria no total de despesas.

---

## Diagrama (Mermaid)

```mermaid
flowchart LR

    U[Usuário]

    R[Seleciona mês]

    C[Controller Gráficos]

    D["Model Despesa"]

    CAT["Model Categoria"]

    DB[(Banco de Dados)]

    P[Agrupar por Categoria]

    G[Resumo + Gráfico]

    U --> R --> C

    C --> D

    D --> DB

    DB --> CAT

    CAT --> P

    P --> G
```

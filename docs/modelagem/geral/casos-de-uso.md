# Diagrama de Caso de Uso - Sistema FINE

## Descrição
Este diagrama representa as principais funcionalidades do sistema Finance Is Now Easy (FINE), considerando a interação do usuário com o sistema.

## Atores
- Usuário autenticado

## Diagrama

```mermaid
graph TD

    Usuario[Usuário autenticado]

    %% Nível 1
    Usuario --> Financeiro
    Usuario --> Analise
    Usuario --> Controle
    Usuario --> Sistema

    %% Nível 2 - Financeiro
    Financeiro --> Receitas[Receitas]
    Financeiro --> Despesas[Despesas]
    Financeiro --> Lancamentos[Lançamentos]
    Financeiro --> Categorias[Categorias]

    %% Nível 2 - Análise
    Analise --> Relatorios[Relatórios]
    Analise --> Graficos[Gráficos]
    Analise --> Comparativo[Comparativo]
    Analise --> Dashboard[Dashboard]

    %% Nível 2 - Controle
    Controle --> Metas[Metas]
    Controle --> Orcamento[Orçamento]
    Controle --> Filtros[Filtros]

    %% Nível 2 - Sistema
    Sistema --> Personalizacao[Personalização]
    Sistema --> Dados[Persistência de dados]
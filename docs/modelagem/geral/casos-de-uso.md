# Diagrama de Caso de Uso - Sistema FINE

## Descrição
Este diagrama representa as principais funcionalidades do sistema Finance Is Now Easy (FINE), considerando a interação do usuário com o sistema.

## Atores
- Usuário autenticado

## Diagrama

```mermaid
graph TD

    Usuario[Usuário autenticado]

    %% Grupo financeiro
    subgraph Financeiro
        Receitas[Gerenciar receitas]
        Despesas[Gerenciar despesas]
        Lancamentos[Editar/excluir lançamentos]
        Categorias[Gerenciar categorias]
    end

    %% Grupo análise
    subgraph Análise
        Relatorios[Visualizar relatórios]
        Graficos[Visualizar gráficos]
        Comparativo[Comparar meses]
        Dashboard[Visualizar dashboard]
    end

    %% Grupo controle
    subgraph Controle
        Metas[Gerenciar metas financeiras]
        Orcamento[Controle de orçamento]
        Filtros[Filtrar transações]
    end

    %% Grupo sistema
    subgraph Sistema
        Personalizacao[Personalizar interface]
        Dados[Persistência de dados]
    end

    %% Ligações
    Usuario --> Receitas
    Usuario --> Despesas
    Usuario --> Lancamentos
    Usuario --> Categorias

    Usuario --> Relatorios
    Usuario --> Graficos
    Usuario --> Comparativo
    Usuario --> Dashboard

    Usuario --> Metas
    Usuario --> Orcamento
    Usuario --> Filtros

    Usuario --> Personalizacao
    Usuario --> Dados
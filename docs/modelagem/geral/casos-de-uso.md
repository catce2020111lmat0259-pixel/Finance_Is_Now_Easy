# Diagrama de Caso de Uso - Sistema FINE

## Descrição
Este diagrama representa as principais funcionalidades do sistema Finance Is Now Easy (FINE), considerando a interação do usuário com o sistema.

## Atores
- Usuário autenticado

## Diagrama

```mermaid
graph LR

    %% Lado esquerdo
    subgraph Esquerda
        Receitas[Gerenciar receitas]
        Despesas[Gerenciar despesas]
        Lancamentos[Editar/excluir lançamentos]
        Categorias[Gerenciar categorias]
        Relatorios[Visualizar relatórios]
        Graficos[Visualizar gráficos]
    end

    %% Centro
    Usuario[Usuário autenticado]

    %% Lado direito
    subgraph Direita
        Comparativo[Comparar meses]
        Metas[Gerenciar metas financeiras]
        Orcamento[Controle de orçamento]
        Dashboard[Visualizar dashboard]
        Filtros[Filtrar transações]
        Personalizacao[Personalizar interface]
        Dados[Persistência de dados]
    end

    %% Conexões esquerda
    Usuario --> Receitas
    Usuario --> Despesas
    Usuario --> Lancamentos
    Usuario --> Categorias
    Usuario --> Relatorios
    Usuario --> Graficos

    %% Conexões direita
    Usuario --> Comparativo
    Usuario --> Metas
    Usuario --> Orcamento
    Usuario --> Dashboard
    Usuario --> Filtros
    Usuario --> Personalizacao
    Usuario --> Dados
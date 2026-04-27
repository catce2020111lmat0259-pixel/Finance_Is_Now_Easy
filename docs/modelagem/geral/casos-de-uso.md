# Diagrama de Caso de Uso - Sistema FINE

## Descrição
Este diagrama representa as principais funcionalidades do sistema Finance Is Now Easy (FINE), considerando a interação do usuário com o sistema.

## Atores
- Usuário autenticado

## Diagrama

```mermaid
## Diagrama

```mermaid
flowchart LR

    Usuario["Usuário autenticado"]

    Usuario --> Receitas["Gerenciar receitas"]
    Usuario --> Despesas["Gerenciar despesas"]
    Usuario --> Lancamentos["Editar/excluir lançamentos"]
    Usuario --> Categorias["Gerenciar categorias"]
    Usuario --> Relatorios["Visualizar relatórios"]
    Usuario --> Graficos["Visualizar gráficos"]

    Usuario --> Comparativo["Comparar meses"]
    Usuario --> Metas["Gerenciar metas financeiras"]
    Usuario --> Orcamento["Controle de orçamento"]
    Usuario --> Dashboard["Visualizar dashboard"]
    Usuario --> Filtros["Filtrar transações"]
    Usuario --> Personalizacao["Personalizar interface"]
    Usuario --> Dados["Persistência de dados"]
# Fluxo da Funcionalidade - HU09 (Metas Financeiras)

## Descrição
Este documento apresenta o fluxo da funcionalidade de criação, edição, exclusão e acompanhamento de metas financeiras, conforme definido na HU09 do Product Backlog.

## Responsável
Gabriel Lopes

## História de Usuário
Como usuário do sistema, quero criar e personalizar metas financeiras, para organizar melhor meus objetivos e acompanhar o progresso em relação aos gastos.

---

## Fluxo da Funcionalidade

O fluxo da funcionalidade de metas segue as etapas abaixo:

1. Usuário acessa a área de metas
2. Sistema exibe a listagem de metas cadastradas
3. Usuário pode optar por criar uma nova meta
4. Sistema exibe o formulário de criação
5. Usuário preenche os dados da meta
6. Sistema realiza normalização e validação dos dados
7. Se válido, o sistema salva a meta no banco de dados
8. Se inválido, o sistema retorna erros ao usuário
9. Sistema atualiza a listagem de metas
10. Usuário pode editar uma meta existente
11. Usuário pode excluir uma meta existente
12. Sistema solicita confirmação antes da exclusão
13. Sistema executa a exclusão e atualiza a listagem

---

## Diagrama (Mermaid)

```mermaid
flowchart LR
    U[Usuário autenticado]

    %% Criar
    R1[GET /fine/metas/criar]
    C1[Controller criar_meta]
    V1[View form-criar-meta.html]

    R2[POST /fine/metas/salvar]
    C2[Controller salvar_meta]

    %% Model e DB
    M[Model Meta (clean + validate)]
    D[(Database - SQLite / SQLAlchemy)]

    %% Listagem
    L[View lista de metas]

    %% Ações
    E[Editar meta]
    EX[Excluir meta]
    CONF[Confirmação de exclusão]

    %% Fluxo criação
    U --> R1 --> C1 --> V1
    U -->|Envia formulário| R2 --> C2 --> M

    M -->|Dados válidos| D
    M -->|Dados inválidos| C2
    D --> C2 --> L

    %% Fluxo listagem
    U --> L

    %% Editar
    L -->|Clique editar| E --> V1

    %% Excluir
    L -->|Clique excluir| CONF
    CONF -->|Confirmar| EX --> D --> L
    CONF -->|Cancelar| L
# Modelo Entidade-Relacionamento

## Descrição

Este documento apresenta o Modelo Entidade-Relacionamento (MER) do FINE, representando as principais entidades do sistema e seus relacionamentos.

---

## Diagrama (Mermaid)

```mermaid
flowchart LR

    Usuario["Usuário"]

    Receita["Receita"]
    Despesa["Despesa"]
    Categoria["Categoria"]
    Meta["Meta"]

    Usuario -- "1:N" --> Receita
    Usuario -- "1:N" --> Despesa
    Usuario -- "1:N" --> Categoria
    Usuario -- "1:N" --> Meta

    Categoria -- "1:N" --> Receita
    Categoria -- "1:N" --> Despesa
```

---

## Entidades

### Usuário
- id (PK)
- nome
- email
- senha
- data_nascimento
- pergunta_secreta
- resposta_secreta

### Categoria
- id (PK)
- nome
- descricao
- tipo
- cor
- padrao
- usuario_id (FK)

### Receita
- id (PK)
- valor
- data
- descricao
- recebido
- usuario_id (FK)
- categoria_id (FK)

### Despesa
- id (PK)
- valor
- data
- descricao
- pago
- usuario_id (FK)
- categoria_id (FK)

### Meta
- id (PK)
- conteudo
- fixada
- usuario_id (FK)
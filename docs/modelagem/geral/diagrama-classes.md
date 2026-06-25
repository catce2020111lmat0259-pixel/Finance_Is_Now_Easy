# Diagrama de Classes

## Descrição

Este documento apresenta o Diagrama de Classes do FINE (Finance Is Now Easy), representando as principais entidades do sistema e seus relacionamentos conforme a arquitetura MVC implementada.

As classes apresentadas correspondem aos modelos responsáveis pela persistência dos dados da aplicação.

---

## Classes

- Usuario
- Receita
- Despesa
- Categoria
- Meta

---

## Diagrama (Mermaid)

```mermaid
classDiagram

class Usuario{
    +id : int
    +nome : string
    +email : string
    +senha : string
    +data_nascimento : date
    +pergunta_secreta : string
    +resposta_secreta : string
}

class Categoria{
    +id : int
    +nome : string
    +descricao : string
    +tipo : string
    +cor : string
    +padrao : bool
    +usuario_id : int
}

class Receita{
    +id : int
    +valor : decimal
    +data : date
    +descricao : string
    +recebido : bool
    +usuario_id : int
    +categoria_id : int
}

class Despesa{
    +id : int
    +valor : decimal
    +data : date
    +descricao : string
    +pago : bool
    +usuario_id : int
    +categoria_id : int
}

class Meta{
    +id : int
    +conteudo : string
    +fixada : bool
    +usuario_id : int
}

Usuario "1" --> "*" Receita
Usuario "1" --> "*" Despesa
Usuario "1" --> "*" Categoria
Usuario "1" --> "*" Meta

Categoria "1" --> "*" Receita
Categoria "1" --> "*" Despesa
```

---

## Descrição dos Relacionamentos

- Um usuário pode possuir diversas receitas.
- Um usuário pode possuir diversas despesas.
- Um usuário pode possuir diversas categorias.
- Um usuário pode possuir diversas metas.
- Uma categoria pode classificar várias receitas.
- Uma categoria pode classificar várias despesas.

---

## Observações

O diagrama representa as principais classes responsáveis pela persistência de dados da aplicação, implementadas utilizando SQLAlchemy. Cada usuário possui seu próprio conjunto de categorias, receitas, despesas e metas, garantindo isolamento das informações entre diferentes contas.
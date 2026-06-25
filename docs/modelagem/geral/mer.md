erDiagram
    USUARIO ||--o{ RECEITA : possui
    USUARIO ||--o{ DESPESA : possui
    USUARIO ||--o{ CATEGORIA : possui
    USUARIO ||--o{ META : possui

    CATEGORIA ||--o{ RECEITA : classifica
    CATEGORIA ||--o{ DESPESA : classifica

    USUARIO {
        int id PK
        string nome
        string email UK
        string senha
        date data_nascimento
        string pergunta_secreta
        string resposta_secreta
    }

    CATEGORIA {
        int id PK
        string nome
        string descricao
        string tipo
        string cor
        boolean padrao
        int usuario_id FK
    }

    RECEITA {
        int id PK
        decimal valor
        date data
        string descricao
        boolean recebido
        int usuario_id FK
        int categoria_id FK
    }

    DESPESA {
        int id PK
        decimal valor
        date data
        string descricao
        boolean pago
        int usuario_id FK
        int categoria_id FK
    }

    META {
        int id PK
        string conteudo
        boolean fixada
        int usuario_id FK
    }
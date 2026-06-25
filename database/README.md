# Banco de Dados

Esta pasta reúne os principais artefatos relacionados à estrutura do banco de dados do projeto **FINE (Finance Is Now Easy)**.

## Arquivos

### `fine_schema.sql`

Definição da estrutura do banco de dados, incluindo a criação das tabelas, chaves primárias, chaves estrangeiras e relacionamentos entre as entidades do sistema.

### `fine_seeds.sql`

Dados iniciais de exemplo para auxiliar na compreensão da estrutura do banco, incluindo um usuário, categorias padrão e uma meta financeira.

### `modelo_er.png`

Apresenta o Modelo Entidade-Relacionamento (MER) do sistema, ilustrando as entidades, atributos e relacionamentos existentes entre elas.

## Tecnologias

- SQLite (utilizado durante o desenvolvimento)
- SQLAlchemy (ORM utilizado pela aplicação Flask)
- PostgreSQL (planejado para futuras versões)

## Principais Entidades

- Usuário
- Categoria
- Receita
- Despesa
- Meta

## Observações

Embora o projeto utilize o SQLAlchemy para criação e gerenciamento das tabelas, os arquivos SQL presentes nesta pasta representam a estrutura lógica do banco de dados implementado, servindo como documentação e referência da modelagem utilizada pelo sistema.
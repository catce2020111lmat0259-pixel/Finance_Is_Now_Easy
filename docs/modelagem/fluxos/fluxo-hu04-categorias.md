# Fluxo da Funcionalidade - HU04 (Gerenciamento de Categorias)

## Descrição
Este documento descreve o fluxo completo da funcionalidade de gerenciamento de categorias, incluindo criação, edição, desativação, reativação e listagem de categorias financeiras.

## Responsável
Manoel Henrique Rodrigues

## História de Usuário
Como usuário autenticado, quero criar e gerenciar categorias para classificar minhas receitas e despesas, organizando minhas finanças pessoais de forma estruturada.

---

## Definição

Uma categoria representa a natureza financeira de um registro e possui as seguintes características:

- Pertence exclusivamente a um usuário  
- Possui tipo fixo: **receita** ou **despesa**  
- Pode ser desativada (soft delete) sem perda de histórico  
- Pode ser:
  - **Fixa** (criada automaticamente pelo sistema)
  - **Personalizada** (criada pelo usuário)

### Regras estruturais:
- Categorias fixas:
  - Não podem ter o nome editado  
  - Podem ser desativadas e reativadas  

- Categorias personalizadas:
  - Podem ter o nome editado  
  - Podem ser desativadas e reativadas  

---

## Categorias Fixas ou Nativas (Seed automático)

### Tipo: Despesa
- Aluguel  
- Alimentação  
- Transporte  
- Saúde  
- Energia Elétrica  
- Internet  

### Tipo: Receita
- Salário  
- Freelance  
- Investimentos  
- Outros  

---

## Regras de Negócio

- Cada categoria pertence a **um único usuário**
- O tipo (**receita/despesa**) é **imutável**
- Nome deve ser único por (**usuário + tipo**)
- Toda categoria inicia como **ativa**
- Categorias fixas são criadas automaticamente no cadastro do usuário
- Categorias fixas **não podem ser editadas**
- Soft delete via campo `ativa`
- Categorias inativas aparecem apenas na aba **"Inativas"**
- Correção de tipo deve ser feita criando uma nova categoria

---

## Fluxo da Funcionalidade

### Acesso e Seed Inicial
1. Usuário realiza cadastro no sistema  
2. Sistema cria automaticamente as categorias fixas  
3. Todas iniciam com:
   - `ativa = True`
   - `fixa = True`

---

### Listagem de Categorias
4. Usuário acessa (`GET /categorias`)  
5. Sistema exibe duas abas:
   - **Ativas**
   - **Inativas**

6. Aba **Ativas**:
   - Exibe apenas categorias com `ativa = True`
   - Separadas em:
     - Receita
     - Despesa  

7. Aba **Inativas**:
   - Exibe apenas categorias com `ativa = False`

---

### Criação de Categoria
8. Usuário clica em "Nova Categoria"  
9. Sistema exibe formulário (`GET /categorias/nova`)  

10. Usuário informa:
- Nome  
- Tipo (receita ou despesa)  

11. Envio do formulário (`POST /categorias`)  

12. Sistema valida:
- Nome obrigatório  
- Mínimo de 2 caracteres  
- Sem caracteres inválidos  
- Unicidade (usuário + tipo)  

13. Se inválido:
- Retorna erros na view  

14. Se válido:
- Salva com:
  - `fixa = False`
  - `ativa = True`  

15. Atualiza listagem  

---

### Edição de Categoria
16. Usuário clica em editar (`GET /categorias/{id}/editar`)  

17. Sistema verifica:
- Se `fixa = True` → bloqueia edição  
- Se `fixa = False` → permite edição  

18. Usuário altera nome  

19. Envio (`POST /categorias/{id}`)  

20. Sistema valida:
- Nome válido  
- Unicidade  

21. Atualiza registro  

> O tipo da categoria não pode ser alterado

---

### Desativação (Soft Delete)
22. Usuário clica em desativar  
23. Sistema solicita confirmação  

24. Se confirmado:
- Define `ativa = False`  

25. Categoria sai da aba **Ativas** e vai para **Inativas**

---

### Reativação
26. Usuário acessa aba **Inativas**  
27. Usuário clica em reativar  

28. Sistema define:
- `ativa = True`  

29. Categoria volta para aba **Ativas**

---

### Correção de Tipo
30. Usuário identifica categoria com tipo incorreto  
31. Sistema não permite alteração direta  

32. Usuário deve:
- Criar nova categoria com o tipo correto  

---

## Diagrama (Mermaid)

```mermaid
flowchart LR
    U[Usuário autenticado]

    %% Rotas
    R1[GET /categorias]
    R2[GET /categorias/nova]
    R3[POST /categorias]

    %% Controller
    C1[Controller listar_categorias]
    C2[Controller criar_categoria]
    C3[Controller salvar_categoria]

    %% Model
    M["Model Categoria (validate + regras de negócio)"]

    %% DB
    D[(Database)]

    %% Views
    L[Lista de categorias]
    F[Formulário]

    %% Fluxo principal
    U --> R1 --> C1 --> D --> L

    U --> R2 --> C2 --> F
    U -->|submit| R3 --> C3 --> M

    M -->|válido| D --> C1 --> L
    M -->|inválido| C3 --> F

    %% Editar
    L -->|editar| C2

    %% Desativar
    L -->|desativar| D --> L

    %% Reativar
    L -->|reativar| D --> L

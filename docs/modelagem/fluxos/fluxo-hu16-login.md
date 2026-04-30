# Fluxo da Funcionalidade - HU16 (Autenticação de Usuário - Login)

## Descrição
Este documento descreve o fluxo completo da funcionalidade de autenticação de usuários, incluindo login, controle de sessão e logout.

## Responsável
Manoel Henrique Rodrigues

## História de Usuário
Como usuário não autenticado, quero informar minhas credenciais de acesso para entrar no sistema, garantindo acesso seguro às minhas informações financeiras.

---

## Definição

A autenticação permite validar a identidade do usuário por meio de credenciais previamente cadastradas.

### Características:
- Utiliza **username** e **senha**
- Senha armazenada de forma **criptografada**
- Criação de **sessão ativa** após login
- Controle de sessão para acesso a áreas restritas
- Usuários autenticados não devem acessar a tela de login
- Sessão pode ser encerrada via logout

---

## Regras de Negócio

- Apenas usuários cadastrados podem se autenticar
- O username deve existir no banco
- A senha deve corresponder ao hash armazenado
- Campos devem ser validados antes da autenticação
- Login bem-sucedido redireciona para área principal
- Sessão permanece ativa até logout ou expiração
- Usuários autenticados não podem acessar `/login`
- Rotas protegidas exigem autenticação
- Logout deve invalidar completamente a sessão

---

## Fluxo da Funcionalidade

### Acesso à tela de login
1. Usuário não autenticado acessa (`GET /login`)  
2. Sistema exibe formulário com:
   - Username  
   - Senha  

---

### Tentativa de autenticação
3. Usuário envia formulário (`POST /login`)  

4. Sistema valida:
- Campos obrigatórios  
- Existência do usuário  
- Senha correta (comparação com hash)  

---

### Falha na autenticação
5. Se campos inválidos:
- Retorna erro de validação  

6. Se usuário não existir:
- Retorna erro informando usuário inválido  

7. Se senha incorreta:
- Retorna erro informando senha inválida  

---

### Sucesso na autenticação
8. Se credenciais válidas:
- Cria sessão do usuário  
- Armazena identificação (ex: `user_id`)  
- Redireciona para área principal (`/dashboard`)  

---

### Controle de sessão
9. Usuário autenticado:
- Pode acessar rotas protegidas  

10. Usuário não autenticado:
- Ao tentar acessar rotas protegidas → redirecionado para `/login`  

---

### Bloqueio da tela de login
11. Usuário autenticado tenta acessar `/login`  
12. Sistema redireciona para `/dashboard`  

---

### Logout
13. Usuário acessa (`GET /logout`)  
14. Sistema:
- Invalida sessão  
- Remove dados de autenticação  
- Redireciona para `/login`  

---

## Critérios de Aceitação

**CA01 — Exibição da tela de login**  
Dado que o usuário não está autenticado  
Quando acessar a rota de login  
Então o sistema deve exibir formulário com username e senha  

**CA02 — Validação de campos obrigatórios**  
Dado que o usuário está na tela de login  
Quando tentar autenticar com campos vazios  
Então o sistema deve impedir a autenticação e exibir erro  

**CA03 — Usuário inexistente**  
Dado que o usuário informa username não cadastrado  
Quando tentar login  
Então o sistema deve impedir e informar erro  

**CA04 — Senha incorreta**  
Dado que o usuário informa username válido  
Quando informar senha incorreta  
Então o sistema deve impedir e informar erro  

**CA05 — Login realizado com sucesso**  
Dado que o usuário informa credenciais válidas  
Quando autenticar  
Então o sistema deve criar sessão ativa e redirecionar  

**CA06 — Controle de sessão**  
Dado que o usuário está autenticado  
Quando acessar páginas protegidas  
Então o sistema deve permitir  

Dado que não está autenticado  
Então deve redirecionar para login  

**CA07 — Bloqueio da tela de login**  
Dado que o usuário já está autenticado  
Quando acessar `/login`  
Então deve ser redirecionado para área principal  

**CA08 — Logout**  
Dado que o usuário está autenticado  
Quando realizar logout  
Então o sistema deve encerrar sessão e redirecionar  

---

## Diagrama (Mermaid)

```mermaid
flowchart LR
    U[Usuário não autenticado]

    %% Rotas
    R1[GET /login]
    R2[POST /login]
    R3[GET /logout]

    %% Controllers
    C1[Controller exibir_login]
    C2[Controller autenticar]
    C3[Controller logout]

    %% Model
    M["Model Usuário (validação + verificação de senha)"]

    %% Sessão
    S[(Session)]

    %% Views
    V1[Formulário de login]
    V2[Dashboard]

    %% Fluxo login
    U --> R1 --> C1 --> V1
    U -->|submit| R2 --> C2 --> M

    M -->|válido| S --> V2
    M -->|inválido| C2 --> V1

    %% Proteção
    S -->|autenticado| V2
    S -->|não autenticado| V1

    %% Logout
    V2 --> R3 --> C3 --> S --> V1

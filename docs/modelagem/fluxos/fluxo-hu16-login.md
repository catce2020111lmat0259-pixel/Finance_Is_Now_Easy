# Fluxo da Funcionalidade - HU16 (Login e Validação)

## Descrição
Este documento apresenta o fluxo da funcionalidade de cadastro, autenticação e encerramento de sessão de usuários, conforme definido na HU16 do Product Backlog.

## Responsável
Manoel Henrique Rodrigues

## História de Usuário
Como visitante/usuário, quero me cadastrar, autenticar e encerrar sessão com validações adequadas, para acessar o sistema com segurança.

## Fluxo da Funcionalidade
O fluxo da funcionalidade de autenticação segue as etapas abaixo:

Usuário acessa a tela de login ou cadastro  
Sistema exibe o formulário correspondente  

### Cadastro
Usuário preenche usuário e senha  
Usuário confirma a senha  
Sistema realiza validação dos dados  
Sistema verifica se o usuário já existe  

Se válido:  
Sistema salva o usuário no banco de dados  
Sistema redireciona para a tela de login  

Se inválido:  
Sistema retorna mensagens de erro ao usuário  

### Login
Usuário informa usuário e senha  
Sistema valida as credenciais  

Se válido:  
Sistema inicia a sessão do usuário  
Sistema redireciona para o dashboard  

Se inválido:  
Sistema exibe mensagem de erro  

### Logout
Usuário clica no botão "Sair"  
Sistema encerra a sessão do usuário  
Sistema redireciona para a tela de login  

## Diagrama (Mermaid)

```mermaid
flowchart TD
A[Usuário acessa login/cadastro] --> B{Escolha}
B -->|Cadastro| C[Preenche dados]
C --> D[Validação]
D -->|Válido| E[Salva usuário]
E --> F[Redireciona para login]
D -->|Inválido| G[Exibe erro]

B -->|Login| H[Informa credenciais]
H --> I[Validação]
I -->|Válido| J[Cria sessão]
J --> K[Dashboard]
I -->|Inválido| L[Erro]

K --> M[Logout]
M --> N[Encerra sessão]
N --> O[Volta ao login]

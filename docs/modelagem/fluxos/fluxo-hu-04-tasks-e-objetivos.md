# Fluxo da Funcionalidade - HU04 (Tasks e Objetivos)

## Descrição
Este documento apresenta o fluxo da funcionalidade de gerenciamento de tarefas e categorias, incluindo criação, edição, exclusão e acompanhamento, conforme definido na HU04 do Product Backlog.

## Responsável
Manoel Henrique Rodrigues

## História de Usuário
Como usuário autenticado, quero gerenciar tarefas e categorias, para organizar e acompanhar meus objetivos.

## Fluxo da Funcionalidade
O fluxo da funcionalidade de tarefas segue as etapas abaixo:

Usuário acessa o dashboard  
Sistema exibe a listagem de tarefas do usuário  

### Criar tarefa
Usuário seleciona criar nova tarefa  
Sistema exibe o formulário de criação  
Usuário preenche título e seleciona categoria  
Sistema realiza validação dos dados  

Se válido:  
Sistema salva a tarefa no banco de dados  
Sistema atualiza a listagem de tarefas  

Se inválido:  
Sistema retorna mensagens de erro ao usuário  

### Listar tarefas
Sistema exibe título, categoria e status (concluída/pendente)  
Sistema garante que apenas tarefas do usuário logado sejam exibidas  

### Filtrar tarefas
Usuário seleciona uma categoria no filtro  
Sistema atualiza a listagem exibindo apenas tarefas da categoria selecionada  
Usuário pode remover o filtro para visualizar todas as tarefas  

### Concluir tarefa
Usuário marca ou desmarca a tarefa  
Sistema atualiza o status da tarefa (concluída/pendente)  
Sistema reflete visualmente tarefas concluídas (ex: texto riscado)  

### Editar tarefa
Usuário seleciona editar tarefa  
Sistema exibe formulário com dados atuais  
Usuário altera o título  
Sistema valida os dados  

Se válido:  
Sistema atualiza a tarefa no banco  
Sistema atualiza a listagem  

Se inválido:  
Sistema retorna erro ao usuário  

### Excluir tarefa
Usuário seleciona excluir tarefa  
Sistema solicita confirmação  

Se confirmado:  
Sistema remove a tarefa do banco de dados  
Sistema atualiza a listagem  

### Categorias
Usuário cria nova categoria  
Sistema valida o nome da categoria  

Se válido:  
Sistema salva a categoria  
Sistema atualiza as opções de seleção  

Se inválido:  
Sistema retorna erro  

## Diagrama (Mermaid)

```mermaid
flowchart TD
A[Usuário acessa dashboard] --> B[Listagem de tarefas]

B --> C[Criar tarefa]
C --> D[Preenche dados]
D --> E[Validação]
E -->|Válido| F[Salva tarefa]
F --> B
E -->|Inválido| G[Erro]

B --> H[Filtrar tarefas]
H --> B

B --> I[Concluir tarefa]
I --> B

B --> J[Editar tarefa]
J --> K[Atualiza dados]
K --> B

B --> L[Excluir tarefa]
L --> M{Confirma?}
M -->|Sim| N[Remove tarefa]
N --> B
M -->|Não| B

B --> O[Criar categoria]
O --> P[Validação]
P -->|Válido| Q[Salva categoria]
Q --> B
P -->|Inválido| R[Erro]

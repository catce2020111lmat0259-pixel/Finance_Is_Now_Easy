# Arquitetura do Sistema

## Descrição Geral

O sistema **Finance Is Now Easy (FINE)** segue o padrão arquitetural **MVC (Model-View-Controller)** utilizando o framework Flask.

A aplicação está organizada em camadas que separam responsabilidades, facilitando manutenção, escalabilidade e entendimento do código.

---

## Estrutura do Projeto

A lógica principal da aplicação está concentrada na pasta `backend/`, onde se encontra a estrutura MVC:

```
backend/
├── controllers/   # Lógica de controle das requisições
├── models/        # Estrutura de dados e regras de negócio
├── routes/        # Definição das rotas/endpoints
├── instance/      # Configuração e banco de dados (SQLite)
├── templates/     # Interfaces HTML (Views)
├── static/        # Arquivos CSS, JavaScript, img e fonts
└── main.py        # Ponto de entrada da aplicação
```

---

## Descrição das Camadas

### Controllers

Responsáveis por processar as requisições do usuário, coordenar o fluxo da aplicação e interagir com os models.

### Models

Representam as entidades do sistema e implementam regras de negócio, validações e interação com o banco de dados via SQLAlchemy.

### Routes

Definem os endpoints da aplicação e fazem a ligação entre as requisições HTTP e os controllers.

### Views (Templates)

Responsáveis pela interface com o usuário, utilizando HTML renderizado pelo Flask.

### Static

Contém arquivos estáticos utilizados pela interface do sistema, como:

* Arquivos de estilo (**CSS**)
* Scripts (**JavaScript**)
* Imagens (**img**)
* Fontes personalizadas (**fonts**)

Esses recursos são utilizados pelos templates para compor a interface visual da aplicação.

### Instance

Armazena configurações específicas da aplicação e o banco de dados local (SQLite).

### Main

Arquivo responsável por inicializar e executar a aplicação Flask.

---

## Banco de Dados

O sistema utiliza:

* SQLite (ambiente local)
* PostgreSQL (planejado para deploy em ambiente web via Render)

A comunicação com o banco é feita através do **SQLAlchemy**.

---

## Fluxo de Funcionamento

1. O usuário interage com a interface (HTML)
2. A requisição é enviada para uma rota
3. A rota direciona para um controller
4. O controller processa a lógica
5. O model valida os dados e interage com o banco
6. O resultado é retornado ao usuário via template

---

## Diagrama de Arquitetura

Ainda não foi gerado um diagrama visual.

Será criado na próxima etapa e disponibilizado em:

`docs/modelagem/arquitetura.png`

Responsável: Equipe
Status: Em desenvolvimento
Previsão: Sprint 4

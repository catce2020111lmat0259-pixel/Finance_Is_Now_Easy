# Arquitetura do Sistema

## Descrição Geral

O sistema **Finance Is Now Easy (FINE)** segue o padrão arquitetural **MVC (Model-View-Controller)** utilizando o framework Flask.

A aplicação está organizada em camadas que separam responsabilidades, facilitando manutenção, escalabilidade e entendimento do código.

---

## Estrutura do Projeto

A lógica principal da aplicação está concentrada na pasta `backend/`, onde se encontra a estrutura MVC:

---

## Descrição das Camadas

### Routes

Definem os endpoints da aplicação e fazem a ligação entre as requisições HTTP e os controllers.

---

### Controllers

Responsáveis por processar as requisições do usuário, coordenar o fluxo da aplicação e interagir com os models.

Também são responsáveis por retornar a resposta ao usuário, geralmente através da renderização de templates.

---

### Models

Representam as entidades do sistema e são responsáveis pela estruturação dos dados e interação com o banco de dados através do SQLAlchemy.

---

### Views (Templates)

Responsáveis pela interface com o usuário, utilizando HTML renderizado pelo Flask.

---

### Static

Contém arquivos estáticos utilizados pela interface do sistema, como:

* Arquivos de estilo (**CSS**)
* Scripts (**JavaScript**)
* Imagens (**img**)
* Fontes (**fonts**)

---

### Instance

Armazena configurações específicas da aplicação e o banco de dados local (SQLite).

---

### Main

Arquivo responsável por inicializar e executar a aplicação Flask.

---

## Banco de Dados

O sistema utiliza:

* SQLite (ambiente local)
* PostgreSQL (planejado para deploy em ambiente web)

A comunicação com o banco é feita através do **SQLAlchemy**.

---

## Fluxo de Funcionamento

1. O usuário interage com a interface (Frontend)
2. A requisição é enviada para uma rota
3. A rota direciona para um controller
4. O controller processa a lógica da aplicação
5. O model interage com o banco de dados
6. O resultado é retornado ao usuário via template

---

## Diagrama de Arquitetura

O diagrama abaixo representa a arquitetura do sistema FINE, destacando a separação em camadas (Frontend, Backend e Banco de Dados) e a organização interna do backend no padrão MVC.

![Arquitetura do Sistema](docs/modelagem/geral/arquitetura.png)

Responsável: Equipe  
Status: Concluído  
📌 Visão Geral

A FinLead API é uma aplicação backend desenvolvida em Python + Flask, estruturada em camadas e preparada para escalar.
Ela cobre autenticação, regras de negócio e persistência de dados, servindo como base para CRMs, sistemas de prospecção e dashboards analíticos.

🧱 Arquitetura

O projeto segue uma arquitetura em camadas:

Controllers: responsáveis por lidar com HTTP (request/response)

Services: concentram as regras de negócio

Models: representam as entidades do banco de dados

Utils: funções utilitárias compartilhadas

Config: configuração de ambiente e banco

Separação clara de responsabilidades, facilitando manutenção e evolução.

🗂 Estrutura de Pastas
ProjetoFUTURO/
├── app.py                 # Bootstrap da aplicação Flask
├── config.py              # Configurações e banco de dados
├── controllers/           # Controllers (rotas HTTP)
│   └── authController.py
├── services/              # Regras de negócio
│   └── authService.py
├── models/                # Models SQLAlchemy
│   └── user.py
├── utils/                 # Helpers e respostas padrão
│   └── response.py
├── migrations/            # Migrations (Alembic)
├── .env                   # Variáveis de ambiente
├── requirements.txt
└── README.md

🔐 Autenticação
POST /auth/register

Criação de usuários do sistema (ex: gestor, vendedor).

Request body

{
  "nome": "Guilherme",
  "email": "guilherme@email.com",
  "senha": "123456",
  "role": "gestor"
}


Response

{
  "success": true,
  "message": "Usuário criado com sucesso",
  "data": {
    "id": 1,
    "nome": "Guilherme",
    "email": "guilherme@email.com",
    "role": "gestor"
  }
}

POST /auth/login

Autenticação de usuários cadastrados.

Request body

{
  "email": "guilherme@email.com",
  "senha": "123456"
}


Response

{
  "success": true,
  "message": "Login realizado com sucesso",
  "data": {
    "id": 1,
    "nome": "Guilherme",
    "email": "guilherme@email.com",
    "role": "gestor"
  }
}

⚙️ Tecnologias

Python 3.12+

Flask

Flask-SQLAlchemy

Flask-Migrate (Alembic)

PostgreSQL

Postman

Git / GitHub

Deploy planejado: Render

🗄 Banco de Dados

PostgreSQL

Versionamento de schema via Flask Migrate

Migrations aplicadas com segurança em ambiente local e produção

▶️ Executando o projeto localmente
1. Clonar o repositório
git clone https://github.com/seu-usuario/finlead-api.git
cd finlead-api

2. Criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

3. Instalar dependências
pip install -r requirements.txt

4. Configurar variáveis de ambiente

Crie um arquivo .env:

DATABASE_URL=postgresql://usuario:senha@localhost:5432/finlead
SECRET_KEY=dev123

5. Aplicar migrations
flask db upgrade

6. Iniciar a aplicação
python app.py


A API estará disponível em:

http://127.0.0.1:5000

📊 Roadmap
Fase Atual

 Estrutura base do projeto

 Autenticação (login e registro)

 Organização em camadas

Próximas Etapas

 CRUD de Leads financeiros

 Regras de score e priorização

 Métricas para dashboard

 JWT para autenticação

 Deploy no Render

👤 Autor

Guilherme Dartora
Projeto desenvolvido com foco em backend, arquitetura de APIs e mercado financeiro, visando portfólio profissional e processos seletivos.
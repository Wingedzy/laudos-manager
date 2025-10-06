# 📝 Laudos Manager

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-green)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistema de **agendamento e emissão de laudos de capacidade técnica**, desenvolvido com **Python**, **FastAPI**, **SQLAlchemy** e banco de dados **PostgreSQL**.  

---

## 🚀 Funcionalidades

- Cadastro e gerenciamento de candidatos
- Agendamento de emissão de laudos
- Banco de dados PostgreSQL
- Estrutura pronta para integração com Google Agenda (opcional)
- Código organizado e pronto para deploy

---

## 🗂 Estrutura do Projeto

.
├── app/
│ ├── init.py
│ ├── config.py # Configurações do projeto e variáveis de ambiente
│ ├── database.py # Conexão com PostgreSQL
│ ├── models.py # Modelos SQLAlchemy
│ └── routes/
│ ├── init.py
│ ├── agendamento.py # Endpoints de agendamento
│ └── candidatos.py # Endpoints de candidatos
├── alembic/ # Migrations do banco
├── .env.example # Exemplo de arquivo de variáveis de ambiente
├── requirements.txt # Dependências do projeto
├── main.py # Arquivo principal da aplicação
├── README.md
└── teste_db.py # Teste de conexão com PostgreSQL

yaml
Copiar código

---

## ⚙️ Configuração

1. Crie um arquivo `.env` copiando o `.env.example`:

```bash
cp .env.example .env
Preencha as variáveis:

env
Copiar código
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nome_do_banco
Instale as dependências:

bash
Copiar código
pip install -r requirements.txt
🏃‍♂️ Rodando o Projeto
Ative o ambiente virtual:

bash
Copiar código
source venv/Scripts/activate  # Windows (Git Bash)
# ou
source venv/bin/activate      # Linux / macOS
Execute a aplicação:

bash
Copiar código
uvicorn main:app --reload
Abra o navegador e acesse:
http://127.0.0.1:8000

Documentação automática da API:
http://127.0.0.1:8000/docs (Swagger UI)

🧪 Testando Conexão com Banco
bash
Copiar código
python teste_db.py
Saída esperada:

Copiar código
Conexão com PostgreSQL funcionando!

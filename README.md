# 🧽 Tastur Connect

Sistema de gerenciamento para uma empresa de turismo, desenvolvido com Django e PostgreSQL. O sistema permite o gerenciamento de **clientes**, **parceiros**, **colaboradores** e **reservas**, com acesso via painel administrativo e interfaces separadas para clientes e colaboradores.

---

## 📌 Visão Geral

O projeto tem como objetivo facilitar o controle de reservas e dados de clientes e parceiros da empresa. Ele foi construído em Django com banco de dados PostgreSQL, e utiliza um painel de administração para gestão dos dados.

---

## 📁 Estrutura do Projeto

Aplicativos principais:

* **core**: Gerencia autenticação, login e funcionalidades centrais.
* **clientes**: Cadastro e gerenciamento de clientes.
* **parceiros**: Cadastro e gerenciamento de parceiros.
* **reservas**: Cadastro e gerenciamento de reservas.

---

## 🛠 Requisitos do Sistema

* Python **3.10** ou superior
* Docker + Docker Compose
* PostgreSQL **14** ou superior (usado via Docker)
* Dependências do projeto no arquivo `requirements.txt`

---

## 📥 Como Instalar e Executar Localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/rgizsilva/tastur.git
cd tastur
```

### 2. Instalar o Python (caso ainda não tenha)

* [Download Python](https://www.python.org/downloads/)

Verifique com:

```bash
python3 --version
```

### 3. Instalar Docker e Docker Compose

* [Instalar Docker](https://docs.docker.com/get-docker/)

Verifique se está instalado:

```bash
docker --version
docker compose version
```

### 4. Subir o banco de dados PostgreSQL com Docker Compose

Certifique-se de que o arquivo `docker-compose.yml` está configurado corretamente e execute:

```bash
docker compose up -d
```

Verifique se o container do banco está rodando:

```bash
docker ps
```

---

## ⚙️ Configurando o Ambiente Python

### 5. Criar e ativar um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
# ou
venv\Scripts\activate      # Windows
```

### 6. Instalar as dependências do projeto

```bash
pip install -r requirements.txt
```

---

## 🐅 Configuração do Banco de Dados

### 7. Criar as tabelas no banco via Django

Execute os seguintes comandos para aplicar as migrações:

```bash
python manage.py makemigrations
python manage.py migrate
```

Esses comandos criam automaticamente todas as tabelas definidas nos modelos Django.

---

## 🔐 Criar Usuário Administrador (superuser)

### 8. Criar usuário admin para acessar o painel Django

```bash
python manage.py createsuperuser
```

Informe:

* **Username**: admin
* **Email**: [admin@tastur.com](mailto:admin@tastur.com) (opcional)
* **Senha**: \*\*\*\*\*\*\*\*\*

Esse usuário será usado para acessar o painel admin e cadastrar colaboradores, clientes, parceiros, etc.

---

## 🚀 Rodar o Servidor de Desenvolvimento

### 9. Iniciar o servidor local

```bash
python manage.py runserver
```

A aplicação estará disponível em:

* Painel Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
* Tela de login geral: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧲 Testar a Aplicação

1. Acesse o painel admin e faça login com o superuser criado.
2. Cadastre **colaboradores**, **clientes**, **parceiros** e **reservas**.
3. Remova ou edite reservas conforme necessário.
4. Teste os fluxos como **usuário cliente** também, fazendo login via **NOME** ou **CPF** .

> ✅ **Importante:** Tanto o colaborador quanto o cliente utilizam o nome de user que você cadastrou para logar no sistema.

---

👤 Adicionar Colaborador
Ao adicionar um colaborador, é necessário criar um usuário associado a ele. Siga os passos abaixo:

Acesse o painel admin: http://127.0.0.1:8000/admin/

Vá para Colaboradores e clique em "Adicionar Colaborador".

Na tela de adição de colaborador, haverá um campo chamado "User".

Clique no ícone de "+" (lado direito do campo "User") para criar um novo usuário.

📥 Tela "Adicionar Usuário"
Preencha os seguintes campos:

Usuário:
Insira o CPF ou outro identificador (até 150 caracteres).
Apenas letras, números e @/./+/-/_ são permitidos.

Autenticação baseada em senha:
Deixe como "Habilitado".

Senha:
A senha deve conter no mínimo 8 caracteres, não ser comum, e não pode ser apenas números.

Confirmação de senha:
Repita a mesma senha.

⚠️ Após salvar o usuário, ele será vinculado automaticamente ao colaborador.

Preencha os demais campos do colaborador normalmente:

Nome completo

Telefone

Clique em Salvar.

---

## 📂 Banco de Dados

O sistema utiliza PostgreSQL como banco de dados, com as seguintes tabelas principais:

* **CLIENTES**: Armazena informações dos clientes
* **PARCEIROS**: Armazena informações dos parceiros
* **RESERVAS**: Armazena informações das reservas
* **COLABORADORES**: Armazena informações dos colaboradores (funcionários)

---

## 📊 Tecnologias Utilizadas

* Django 5.2
* PostgreSQL
* Bootstrap 5
* Crispy Forms
* JavaScript
* Docker & Docker Compose

---

## 🛠️ Manutenção

### Backup do Banco de Dados

```bash
pg_dump -U tastur_user -d tastur_db > backup.sql
```

### Restauração do Banco de Dados

```bash
psql -U tastur_user -d tastur_db < backup.sql
```

### Atualização de Dependências

```bash
pip install -r requirements.txt --upgrade
```

---

## 📄 Licença

Este projeto é de código aberto sob a licença MIT.

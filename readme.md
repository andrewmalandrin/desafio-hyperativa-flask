# Desafio Hyperativa

## Descrição

Código criado para o desafio proposto pela Hyperativa de criação de API

## Requisitos

- Python >= 3.11 instalado
- Banco de dados postgresql instalado, configurado e com as tabelas user e card criadas no schema public com os campos abaixo:

**user**

id: bigint + not null + pk

name: character varying(30) + not null

email: character varying(320) + not null

password: character varying(255) + not null

**card**

id: bigint + not null + pk 	

card_number: bigint + not null

batch_number: character varying(8) + not null

batch_date: date + not null

batch_name: character varying(30) + not null

batch_position: smallint + not null

### Documentos/Referências
- Python beginners guide: [https://wiki.python.org/moin/BeginnersGuide](https://wiki.python.org/moin/BeginnersGuide)
- Instalação do postgre: [https://www.w3schools.com/postgresql/postgresql_install.php](https://www.w3schools.com/postgresql/postgresql_install.php)
- Documentação oficial postgre: [https://www.postgresql.org/docs/current/index.html](https://www.postgresql.org/docs/current/index.html)
- Documentação pgadmin 4 : [https://www.pgadmin.org/docs/](https://www.pgadmin.org/docs/)
- Documentação criação de tabelas pelo pgadmin 4: [https://www.pgadmin.org/docs/pgadmin4/8.5/table_dialog.html](https://www.pgadmin.org/docs/pgadmin4/8.5/table_dialog.html)
- Guia acessando o postgresql: [https://www.javatpoint.com/connect-to-a-postgresql-database-server](https://www.javatpoint.com/connect-to-a-postgresql-database-server)
- Guia criando tabela no postgresql: [https://www.javatpoint.com/postgresql-create-table](https://www.javatpoint.com/postgresql-create-table)
- Documentação oficial SQLAlchemy ORM: [https://docs.sqlalchemy.org/orm/](https://docs.sqlalchemy.org/orm/)
- Documentação oficial Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)

## Uso

Após clonar o projeto, abra o git bash na pasta do projeto e crie um ambiente virtual:

    python -m venv .venv

Para ativar o ambiente virtual no windows:

    source .venv/Scripts/activate

No Linux:

    source .venv/bin/activate

Com o ambiente ativo, instale as libs presentes no arquivo requirements.txt

    pip intall -r requirements.txt

Na sequência preencha as configurações no arquivo config/config.json e execute o arquivo main.py

    python main.py

## Endpoints

O flask será servido na porta 5000, no localhost, utilize a url abaixo para envio das requisições

    http://localhost:5000

### Autenticação

Antes de tudo, para a maioria dos endpoints, com exceção do endpoint de registro de novo usuário e o endpoint de login, é necessário possuir o token jwt do usuário.

Para cadastrar um novo usuário use o endpoint de criação de usuário.

**/user/create**

Método: POST

exemplo de payload:

    {
        "name": "Pedro",
        "email": "pedro@teste.com",
        "password": "PcfJky21*"
    }

- name(str): Nome, com no máximo 30 caracteres
- email(str): Email com no máximo 320 caracteres
- password(str): Senha com entre 8 e 10 caracteres, com pelo menos uma letra maiúscula, uma letra minúscula, um número e um caracter especial

Para obtenção do token temos o endpoint /user/auth que é o endpoint de login

**/user/auth**

Método: POST

exemplo de payload:

    {
        "email": "pedro@teste.com",
        "password": "PcfJky21*"
    }

- email(str): Email do usuário
- password(str): Senha do usuário

exemplo de resposta:

    {
        "data": {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxfQ.N1c2nJo8nCgnpvmf1dYSNq_0tqzl9gs_SBG_aDhVCkE"
        },
        "message": "Usuário autenticado"
    }

- token(str): Token jwt para acesso aos demais endpoints
- message(str): Mensagem de retorno
- error(str): Caso ocorra algum erro, será retornado no campo 'error'

### Chamadas

Para realizar chamadas para os endpoints, envie uma request para o endpoint

**/card/create**

Cadastro de novos cartões individualmente

Método: POST

exemplo de payload:

    {
        "card_number": 4456897999999991
    }

- card_number(Int): número do cartão 

exemplo de resposta:

    {
        "data": {
            "card_number": 1234567891011
        },
        "message": "OK"
    }

- card_number: Número do cartão cadastrado
- message: Mensagem de retorno
- error: Caso ocorra algum erro, será retornado no campo 'error'

**/card/create/batch**

Este endpoint recebe um arquivo como parâmetro, para isto, no postman ou ferramenta de sua escolha envie o arquivo como form-data ao invés de json em texto

Método: POST

payload:

key: txt_file

value: arquivo txt

exemplo de resposta:

    {
        "data": {
            "cards": [
                {
                    "card_number": "4456897999999999",
                    "error": "Error: card with number 4456897999999999 already exists",
                    "status": "error"
                },(...)
                (...){
                    "card_number": "4456897919999999",
                    "error": "Error: card with number 4456897919999999 already exists",
                    "status": "error"
                }
            ]
        },
        "message": "OK"
    }

- card_number: Número do cartão cadastrado
- status: Informa se o card foi ou não cadastrado
- message: Mensagem de retorno
- error: Caso ocorra algum erro, será retornado no campo 'error'

**/card**

Método: GET

query_parameters:
- card_number: Número do cartão cadastrado

exemplo de resposta:

    {
        "data": {
            "batch_date": "Thu, 24 May 2018 00:00:00 GMT",
            "batch_name": "DESAFIO-HYPERATIVA",
            "batch_number": "LOTE0001",
            "batch_row_id": 2,
            "card_number": 4456897999999999
        },
        "message": "OK"
    }

- card_number: Número do cartão
- batch_date: Data do lote
- batch_name: Nome do lote
- batch_number: Número do lote
- batch_row_id: Numeração no lote
- message: Mensagem de retorno
  
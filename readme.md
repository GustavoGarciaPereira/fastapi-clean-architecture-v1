# Estudo de Arquitetura Escalável com FastAPI

Este repositório é o resultado de um estudo prático sobre a construção de APIs escaláveis, robustas e de fácil manutenção utilizando **FastAPI**. O foco principal não é a complexidade da regra de negócio, mas sim a aplicação de um conjunto de princípios e boas práticas de arquitetura de software.

O projeto serve como um *blueprint* ou template para iniciar novas aplicações, garantindo que a base de código seja limpa, testável e performática desde o início.

## Princípios de Arquitetura Aplicados

A estrutura e o código deste projeto foram guiados pelos seguintes princípios:

-   **Modularidade**: A aplicação é dividida em componentes claros e com responsabilidades únicas (routers, schemas, utils), facilitando a manutenção e o crescimento.
-   **Programação Funcional e Declarativa**: Preferência por funções puras e rotas declarativas, evitando o uso de classes onde não são estritamente necessárias.
-   **Tipagem Estrita e Validação**: Uso intensivo de type hints e modelos Pydantic para garantir a integridade dos dados na entrada e saída da API.
-   **Padrão RORO (Receive an Object, Return an Object)**: As rotas recebem e retornam modelos Pydantic, tornando o contrato da API explícito e seguro.
-   **Tratamento de Erros Proativo**: Uso de *Guard Clauses* e retornos antecipados para validar condições e tratar erros no início das funções, mantendo o "caminho feliz" limpo e legível.
-   **Operações Assíncronas**: Todas as operações de I/O (como chamadas ao banco de dados) são assíncronas (`async/await`) para maximizar a performance e o throughput.
-   **Injeção de Dependências**: O sistema de injeção de dependências do FastAPI é utilizado para gerenciar recursos, como sessões de banco de dados.
-   **Estrutura de Projeto Clara**: A organização de arquivos e diretórios segue uma convenção lógica que separa as diferentes camadas da aplicação.

## Estrutura do Projeto

```
/fastapi-blueprint
|-- /app
|   |-- /routers
|   |   `-- user_routes.py      # Define os endpoints da API
|   |-- /types
|   |   `-- user_schemas.py     # Contém os modelos Pydantic (schemas)
|   |-- /utils
|   |   `-- database.py         # Configuração da conexão com o banco
|   `-- main.py                 # Ponto de entrada da aplicação FastAPI
|
|-- .env                        # Arquivo para variáveis de ambiente (não versionado)
|-- docker-compose.yml          # Orquestra o serviço do banco de dados
|-- requirements.txt            # Dependências Python do projeto
`-- README.md                   # Esta documentação
```

## Tecnologias Utilizadas

-   **Framework**: FastAPI
-   **Validação de Dados**: Pydantic V2
-   **ORM e Conexão com DB**: SQLAlchemy 2.0 (com suporte a AsyncIO)
-   **Driver do Banco de Dados**: AsyncPG
-   **Banco de Dados**: PostgreSQL 15
-   **Containerização**: Docker & Docker Compose
-   **Servidor ASGI**: Uvicorn

## Configuração do Ambiente

Siga os passos abaixo para configurar e executar o projeto localmente.

### Pré-requisitos

-   Python 3.10+
-   Docker e Docker Compose

### 1. Clone o Repositório

```bash
git clone <url-do-seu-repositorio>
cd fastapi-blueprint
```

### 2. Banco de Dados com Docker

O banco de dados PostgreSQL é gerenciado pelo Docker Compose para garantir um ambiente isolado e consistente.

```bash
# Este comando irá iniciar o container do PostgreSQL em background
docker-compose up -d
```

### 3. Configure a Aplicação

Crie um ambiente virtual e instale as dependências.

```bash
# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 4. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto, copiando o exemplo abaixo. Este arquivo será lido pela aplicação para se conectar ao banco de dados.

**Arquivo: `.env`**
```env
# A aplicação (rodando localmente) se conecta ao 'localhost' porque a porta
# do container Docker está mapeada para a sua máquina.
DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/db_name"
```
> **Nota**: As credenciais (`user`, `password`, `db_name`) devem ser as mesmas definidas no arquivo `docker-compose.yml`.

## Executando a Aplicação

Com o banco de dados rodando e o ambiente configurado, inicie o servidor Uvicorn:

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.

## Documentação da API

O FastAPI gera automaticamente a documentação interativa da API. Após iniciar o servidor, acesse:

-   **Swagger UI**: `http://127.0.0.1:8000/docs`
-   **ReDoc**: `http://127.0.0.1:8000/redoc`
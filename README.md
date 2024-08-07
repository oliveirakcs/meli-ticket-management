# Meli Ticket Management System

## Descrição do Projeto

Este projeto é uma aplicação CRUD para gerenciamento de tickets, que inclui categorias, subcategorias e severidade, além de integração com uma API externa e uso de containers Docker.

## Goal

Desenvolver uma aplicação CRUD para gerenciamento de tickets com integração de API externa e containerização usando Docker, seguindo boas práticas de desenvolvimento e documentação.

- **CRUD de Tickets**
  - Criação, leitura, atualização e exclusão de tickets.
  - Associação de tickets a categorias e subcategorias.
  - Validação de severidade de tickets.

- **Categorias e Subcategorias**
  - Hierarquia de categorias com subcategorias aninhadas.

- **Integração com Banco de Dados**
  - Uso de Docker para criar um container do banco de dados.

- **Integração com API Externa**
  - Utilização da JSONPlaceholder API para simular chamadas de API.

## Tecnologias Utilizadas

- Linguagem de Programação: Python
- Banco de Dados: PostgreSQL
- Containerização: Docker
- Frontend: React

## Boas Práticas de Desenvolvimento

- **GitFlow**: Utilizado para gerenciamento de branches.
- **SOLID, DRY, KISS**: Princípios aplicados ao código.
- **Testes**: Testes unitários e de integração para garantir a qualidade.
- **CI/CD**: GitHub Actions para automação de builds e testes.

## Tasks

### 1. Setup do Ambiente de Desenvolvimento

- **Configurar repositório no GitHub**
  - Criar um novo repositório no GitHub para o projeto.
  - Inicializar o repositório com um arquivo `README.md` e `.gitignore` adequado.
  - Configurar GitFlow para gerenciamento de branches.

- **Configurar GitHub Actions para CI/CD**
  - Criar workflow de CI/CD usando GitHub Actions.
  - Automatizar testes e builds no processo de integração contínua.

- **Configurar o ambiente de desenvolvimento local**
  - Instalar dependências necessárias (Python, Docker, etc.).
  - Configurar um ambiente virtual para o Python.

- **Criar estrutura básica do projeto com Docker Compose**
  - Criar um arquivo docker-compose.yml para definir serviços de aplicação e banco de dados.
  - Configurar Docker para ambiente de desenvolvimento.

### 2. Configuração do Banco de Dados

- **Escolher o banco de dados (PostgreSQL)**
  - Definir a estrutura do banco de dados para tickets, categorias e severidade.
  - Criar um modelo de dados adequado para o projeto.

- **Configurar Docker para o banco de dados**
  - Criar um container Docker para o PostgreSQL.
  - Configurar variáveis de ambiente para o banco de dados.

- **Criar modelo de dados para tickets, categorias e severidade**
  - Definir entidades e relacionamentos no banco de dados.
  - Implementar scripts de migração para o banco de dados.

### 3. Desenvolvimento do Backend

- **Configurar projeto base em Python**
  - Criar estrutura do projeto com FastAPI.
  - Configurar rotas básicas para a API.

- **Implementar API CRUD para Users**
  - Desenvolver endpoints para criação, leitura, atualização e exclusão de usuários.
  - Validar dados de entrada e saída nos endpoints.

- **Implementar API CRUD para Tickets**
  - Desenvolver endpoints para criação, leitura, atualização e exclusão de tickets.
  - Validar dados de entrada e saída nos endpoints.

- **Implementar CRUD para Categorias e Subcategorias**
  - Desenvolver endpoints para gerenciamento de categorias e subcategorias.
  - Implementar lógica de hierarquia de categorias.

- **Implementar lógica de severidade com validação**
  - Adicionar lógica para validação de severidade dos tickets.
  - Impedir a criação de tickets com severidade inválida.

- **Integração com banco de dados externo**
  - Conectar a API ao banco de dados PostgreSQL.
  - Testar operações CRUD com o banco de dados.

### 4. Integração com API Externa

- **Configurar integração com a API JSONPlaceholder**
  - Implementar funcionalidade que consome dados da JSONPlaceholder API.
  - Integrar dados externos no fluxo da aplicação.

### 5. Desenvolvimento do Frontend (Extra)

- **Configurar projeto React**
  - Inicializar projeto React para frontend.
  - Configurar estrutura de pastas e componentes básicos.

- **Criar interface para gerenciamento de tickets**
  - Desenvolver páginas para criação, edição e visualização de tickets.
  - Integrar API backend com o frontend.

- **Criar interface para gerenciamento de categorias e subcategorias**
  - Desenvolver páginas para gerenciamento de categorias.
  - Implementar lógica de hierarquia na interface do usuário.

### 6. Testes e Qualidade

- **Escrever testes unitários para funções críticas**
  - Identificar funções críticas para testes unitários.
  - Implementar testes automatizados para garantir a qualidade.

- **Escrever testes de integração para endpoints da API**
  - Desenvolver testes de integração para endpoints CRUD.
  - Testar interações completas com o banco de dados.

### 7. Documentação e Deployment

- **Escrever documentação detalhada no README.md**
  - Atualizar README.md com instruções de uso e arquitetura.
  - Adicionar detalhes sobre configurações e execução do projeto.

- **Instruções de instalação e configuração**
  - Fornecer passos detalhados para configurar e executar a aplicação.
  - Documentar dependências e variáveis de ambiente necessárias.

- **Descrever métricas para Datadog e New Relic**
  - Detalhar métricas que serão monitoradas no Datadog e New Relic.
  - Explicar o propósito de cada métrica e como elas ajudam na análise da aplicação.

- **Deploy da aplicação em ambiente de produção**
  - Configurar ambiente de produção com Docker.
  - Realizar o deploy final da aplicação.

## Instruções de Instalação

### Backend

1. Clone o repositório usando SSH:
    ```bash
    git clone git@github.com:oliveirakcs/ticket-management.git
    ```

    Nota: Certifique-se de ter uma chave SSH configurada no seu GitHub para realizar o clone via SSH.

2. Configuração do arquivo .env:

    Após clonar o repositório, crie um arquivo .env na raiz do projeto.
    Copie as variáveis de ambiente do arquivo .env.example para o novo arquivo .env.
    Preencha os valores adequados para cada variável de ambiente.

3. Criação do venv:

    Crie um ambiente virtual 
    ```bash
    python -m venv _venv
    ```
    e ative o venv.

4. Instalação das dependencias no _venv:

    Instale os requirements

    ```bash
    pip install -r requirements.txt
    ```

3. Instalação do Pre-Commit:

    Instale o pre-commit na pasta raiz do projeto para garantir a qualidade do código antes de cada commit.
    Execute o seguinte comando para instalar o pre-commit:

    ```bash
      pre-commit install
    ```

    Este setup irá configurar o pre-commit para executar verificações de código usando pylint e black antes de cada commit.

4. Build e execução dos containers Docker:

    Utilize o comando make containers a partir do Makefile para construir e iniciar os containers Docker.

    ```bash
    make containers
    ```

    Isso irá construir os containers, executar automaticamente as migrações, criar o usuário sysadmin (caso não exista) e configurar a API, o banco de dados e o PG Admin.

    Caso precise dar um refresh nos containers, basta usar:

    ```bash
    make restart
    ```

    Por fim, caso deseje subir os containers sem buildar, basta executar:

    ```bash
    make up
    ```

5. Configuração do PG Admin:

    Acesse o PG Admin e crie um novo server.
    Nomeie o server com o mesmo nome definido na variável DB_NAME do arquivo .env.
    No PG Admin, o host do banco de dados deve ser apenas "db".
    Use o usuário e a senha definidos no arquivo .env.

    Assim, o usuário terá acesso à base de dados para gerenciar e visualizar as informações.

6. Execução de Testes:

    Para executar os testes, utilize o seguinte comando:

    ```bash
    make tests
    ```

    Isso irá rodar os testes localizados no diretório especificado.

### Frontend

Este documento fornece as instruções para configurar o ambiente de desenvolvimento para o frontend do projeto.

4. Instalação das Dependências

    Certifique-se de que você tenha o Node.js e o npm instalados em sua máquina. Use o comando abaixo para instalar as dependências necessárias:

    ```bash

    npm install
    ```

    Este comando irá baixar e instalar todas as dependências listadas no arquivo package.json.

5. Executar o Servidor de Desenvolvimento

    Após instalar as dependências, você pode iniciar o servidor de desenvolvimento com o seguinte comando:

    ```bash

    npm start
    ```

    Este comando inicia o aplicativo e abre uma nova aba do navegador apontando para http://localhost:3000 onde o aplicativo React estará em execução.

6. Build para Produção

    Para criar uma versão otimizada do aplicativo para produção, execute:

    ```bash

    npm run build
    ```

    Este comando irá compilar o aplicativo para o diretório build. O build será otimizado para melhor performance e estará pronto para ser implementado.

### Acesso

    API: http://localhost:1201/docs
    A API estará disponível no endereço acima, onde você pode interagir com os endpoints do projeto.

    PGAdmin: http://localhost:5050
    O PGAdmin pode ser acessado neste link para gerenciar e visualizar o banco de dados PostgreSQL
  

## Funcionalidades

### Gerenciamento de Tickets
- **Criação, Edição e Exclusão de Tickets:** Permite que os usuários criem, atualizem e removam tickets facilmente, com validações para garantir a consistência dos dados.
- **Associação de Categorias e Subcategorias:** Cada ticket pode ser associado a categorias e subcategorias específicas, permitindo uma melhor organização e filtragem.
- **Validação de Severidade:** Implementa regras para validar níveis de severidade dos tickets, garantindo que as requisições mais urgentes sejam destacadas e tratadas adequadamente.

### Gestão de Categorias e Subcategorias
- **CRUD de Categorias e Subcategorias:** Oferece uma interface para criar, editar, excluir e visualizar categorias e subcategorias, com suporte a hierarquias aninhadas.
- **Visualização de Estruturas de Categorias:** Os usuários podem expandir e colapsar categorias para explorar a estrutura e detalhes das subcategorias.

### Gerenciamento de Usuários
- **CRUD de Usuários:** Possibilita o gerenciamento de usuários, incluindo criação, edição, exclusão e visualização de perfis de usuários com informações detalhadas.
- **Criação de Usuários Aleatórios:** Funcionalidade para gerar usuários aleatórios via API, facilitando o preenchimento e teste do sistema.

### Interface do Usuário
- **Painel Interativo:** A aplicação inclui um painel intuitivo e responsivo para navegação e gerenciamento de todos os componentes do sistema.
- **Filtros e Pesquisa:** Funcionalidade para pesquisar e filtrar tickets e usuários rapidamente.
- **Notificações e Alertas:** Informações relevantes, como erros ou operações bem-sucedidas, são comunicadas aos usuários por meio de alertas visuais.

### Funcionalidades para Usuários Sysadmin

Os usuários com role de sysadmin têm acesso total ao sistema, permitindo-lhes realizar operações de criação, leitura, atualização e exclusão (CRUD) em todas as áreas do sistema:

- **CRUD de Severidades:** Permite gerenciar os níveis de severidade dos tickets, garantindo que os usuários possam categorizar adequadamente a urgência e a importância dos tickets.

- **CRUD de Tickets:** Os sysadmins podem criar, visualizar, atualizar e deletar tickets, assim como gerenciar as associações de tickets com categorias e subcategorias.

- **CRUD de Usuários:** Permite a criação, edição e exclusão de usuários no sistema. Além disso, os sysadmins podem gerar usuários aleatórios através da integração com a API externa.

- **CRUD de Categorias e Subcategorias:** Os sysadmins têm o poder de gerenciar toda a hierarquia de categorias e subcategorias, permitindo uma organização eficaz dos tickets.

- **Interação com Comentários:** Os usuários podem adicionar comentários aos tickets, com comentários gerados aleatoriamente por meio da integração com a API externa, facilitando discussões sobre cada ticket.

### Funcionalidades para Usuários Comuns

Os usuários com role de user, têm acesso limitado ao sistema, focado no uso prático dos tickets:

- **Criação e Edição de Tickets:** Usuários comuns podem criar novos tickets e editar os tickets que eles criaram. Isso inclui associar tickets a categorias e subcategorias e escolher níveis de severidade apropriados.

- **JSONPlaceholder API:** A aplicação utiliza a API JSONPlaceholder para simular operações externas, incluindo:

  - **Criação de Usuário Aleatório:** Utiliza dados fictícios para gerar usuários aleatórios, permitindo testes e demonstrações sem a necessidade de inserção manual de dados.

  - **Geração de Comentários em Tickets:** Enriquecendo o fluxo de trabalho dos tickets com comentários, simulando interações de usuários.

### Segurança e Autenticação
- **Controle de Acesso:** Implementação de camadas de segurança para controlar o acesso às funcionalidades com base em permissões de usuário.

### Experiência do Usuário
- **Design Responsivo:** O frontend é projetado para se adaptar a diferentes tamanhos de tela.

### Integração com Infraestrutura
- **Docker e Docker Compose:** Utilização de containers Docker para facilitar o desenvolvimento, testes e implantação, garantindo ambientes consistentes.
- **Integração com PostgreSQL:** O sistema utiliza o PostgreSQL como backend para gerenciamento de dados.

### Suporte e Manutenção
- **Testes Automatizados:** Implementação de testes unitários e de integração para garantir a confiabilidade do sistema.


## API Usage Examples

Abaixo estão exemplos de como interagir com a API do Meli Ticket Management System. Certifique-se de incluir o token de autenticação no cabeçalho de cada solicitação.

### Autenticação

Antes de fazer requisições à API, você precisa se autenticar e obter um token de acesso. O token deve ser incluído no cabeçalho de cada requisição.

Exemplo de cabeçalho:

```http
Authorization: Bearer <your_access_token>
```

### Tickets

#### Listar Todos os Tickets

- **Endpoint:** GET /tickets/
- **Authorization:** Required (Scope: read)

```bash

curl -X GET "http://localhost:1201/tickets/" -H "Authorization: Bearer <your_access_token>"
```

- **Response:**

```bash
[
    {
        "id": "a9d8f7ea-b0e7-4f3a-a0f8-c3d34ef8d5a1",
        "title": "Sample Ticket",
        "description": "This is a sample ticket description",
        "categories": [
            {
                "id": "c0f4cfea-7b15-4c5a-bb90-c6b2f891d86a",
                "name": "Category Name"
            }
        ],
        "severity": {
            "id": "d2a2baf3-6d44-4b5d-93e3-ffdf5d4a0e8e",
            "level": 2,
            "description": "Medium severity"
        },
        "status": "ABERTO",
        "comment": "No comments yet",
        "created_at": "2024-08-07T14:32:30.123456",
        "updated_at": null
    }
]
```

#### Criar um Novo Ticket

- **Endpoint:** POST /tickets/
- **Authorization:** Required (Scope: read)

```bash

curl -X POST "http://localhost:1201/tickets/" \
-H "Authorization: Bearer <your_access_token>" \
-H "Content-Type: application/json" \
-d '{
    "title": "New Ticket",
    "description": "Description of the new ticket",
    "category_ids": ["c0f4cfea-7b15-4c5a-bb90-c6b2f891d86a"],
    "severity_id": "d2a2baf3-6d44-4b5d-93e3-ffdf5d4a0e8e",
    "status": "ABERTO"
}'
```

- **Response:**

```bash
{
{
    "id": "e0f3a5f2-4b5e-4c7a-92e5-c3f8b0f7e5a1",
    "title": "New Ticket",
    "description": "Description of the new ticket",
    "categories": [
        {
            "id": "c0f4cfea-7b15-4c5a-bb90-c6b2f891d86a",
            "name": "Category Name"
        }
    ],
    "severity": {
        "id": "d2a2baf3-6d44-4b5d-93e3-ffdf5d4a0e8e",
        "level": 2,
        "description": "Medium severity"
    },
    "status": "ABERTO",
    "comment": null,
    "created_at": "2024-08-07T14:45:30.123456",
    "updated_at": null
}
```

#### Atualizar Ticket

- **Endpoint:** PATCH /tickets/{ticket_id}
- **Authorization:** Required (Scope: read)

```bash

curl -X PATCH "http://localhost:1201/tickets/{ticket_id}" \
-H "Authorization: Bearer <your_access_token>" \
-H "Content-Type: application/json" \
-d '{
    "title": "Updated Ticket Title",
    "status": "EM_PROGRESSO"
}'
```

- **Response:**

```bash

{{
    "id": "e0f3a5f2-4b5e-4c7a-92e5-c3f8b0f7e5a1",
    "title": "Updated Ticket Title",
    "description": "Description of the new ticket",
    "categories": [
        {
            "id": "c0f4cfea-7b15-4c5a-bb90-c6b2f891d86a",
            "name": "Category Name"
        }
    ],
    "severity": {
        "id": "d2a2baf3-6d44-4b5d-93e3-ffdf5d4a0e8e",
        "level": 2,
        "description": "Medium severity"
    },
    "status": "EM_PROGRESSO",
    "comment": null,
    "created_at": "2024-08-07T14:45:30.123456",
    "updated_at": "2024-08-07T15:00:00.123456"
}
```

#### Deletar Ticket

Endpoint: DELETE /tickets/{ticket_id}
Authorization: Required (Scope: admin)

bash

curl -X DELETE "http://localhost:1201/tickets/{ticket_id}" \
-H "Authorization: Bearer <your_access_token>"

- **Response:** HTTP 202 Accepted

#### Adicionar Comentário ao Ticket

- **Endpoint:** POST /tickets/add/{ticket_id}
- **Authorization:** Required (Scope: admin)

```bash

curl -X POST "http://localhost:1201/tickets/add/{ticket_id}" \
-H "Authorization: Bearer <your_access_token>"
```

- **Response:**

```bash
    {
        "message": "Comment added successfully",
        "comment_id": "f3a2b5c7-3e4d-45b6-8c7e-1b8f0f9d7a2b"
    }
```

### Usuários

#### Criar um Usuário Aleatório

- **Endpoint:** POST `/users/create_random_user`
- **Authorization:** Required (Scope: `admin`)

```bash
curl -X POST "http://localhost:1201/users/create_random_user" \
-H "Authorization: Bearer <your_access_token>"
```


- **Response:**

```bash

{
    "id": "f0a2b3c4-d5e6-7f8g-9h0i-1j2k3l4m5n6o",
    "name": "John Doe",
    "username": "johndoe",
    "email": "johndoe@example.com",
    "role": "user"
}

```

### Categorias

#### Criar Nova Categoria com Subcategorias

- **Endpoint:** POST `/categories/`
- **Authorization:** Required (Scope: `admin`)

```bash
curl -X POST "http://localhost:1201/categories/" \
-H "Authorization: Bearer <your_access_token>" \
-H "Content-Type: application/json" \
-d '{
    "name": "Network",
    "subcategories": [
        {
            "name": "Routers"
        },
        {
            "name": "Switches"
        },
        {
            "name": "Access Points"
        }
    ]
}'
```
- **Response:**

```bash
{
    "id": "f1g2h3i4-j5k6-7l8m-9n0o-1p2q3r4s5t6u",
    "name": "Network",
    "subcategories": [
        {
            "id": "a1b2c3d4-e5f6-7g8h-9i0j-1k2l3m4n5o6p",
            "name": "Routers"
        },
        {
            "id": "b1c2d3e4-f5g6-7h8i-9j0k-1l2m3n4o5p6q",
            "name": "Switches"
        },
        {
            "id": "c1d2e3f4-g5h6-7i8j-9k0l-1m2n3o4p5q6r",
            "name": "Access Points"
        }
    ]
}
```

## Descrição dos Diretórios e Arquivos

- **Arquivos de Configuração na Raiz:**

```bash

    .pylintrc: Configuração para o linter Pylint, que ajuda a manter o estilo de código consistente.
    Dockerfile.app: Dockerfile para a criação do container da aplicação.
    requirements.txt: Lista de dependências Python necessárias para o projeto.
    .pre-commit-config.yaml: Configuração para o pre-commit, usado para garantir a qualidade do código antes dos commits.
    alembic.ini: Configuração do Alembic para migrações do banco de dados.
    Makefile: Automação de tarefas comuns como build e teste.
    docker-compose.dev.yml: Configuração do Docker Compose para o ambiente de desenvolvimento.
    docker-compose.test.yml: Configuração do Docker Compose para o ambiente de teste.
    Dockerfile.data: Dockerfile para a criação do container de dados.
    .gitignore: Arquivos e diretórios a serem ignorados pelo Git.
    .env e .env.example: Arquivos de configuração de ambiente para variáveis sensíveis.
    t.py: Script auxiliar ou de teste (nome genérico, depende do conteúdo).

Diretório app/

Contém a aplicação principal e a lógica de negócio.

    main.py: Ponto de entrada da aplicação FastAPI.
    __init__.py: Torna o diretório um pacote Python.

Diretório core/

Componentes centrais e utilitários para a aplicação.

    auth/: Módulo de autenticação.
        jwt_token.py: Manipulação de tokens JWT.
        hashing.py: Funções para hashing de senhas.
        oauth.py: Configuração de OAuth para segurança.
    enums/: Definições de enums para uso na aplicação.
        enums.py: Enums específicos usados no sistema.
    scopes/: Gerenciamento de escopos de autenticação.
        scopes.py: Escopos e permissões definidos.

Diretório tests/

Contém todos os testes unitários e de integração.

    conftest.py: Configurações e fixtures para testes.
    create_test_client.py: Configuração do cliente de teste FastAPI.
    unit/: Testes unitários.
        checker/: Testes relacionados a verificações de código.
        hashing/: Testes para hashing de senhas.
        external/: Testes para funcionalidades externas.
    integration/: Testes de integração para endpoints.

Diretório schemas/

Definições de esquemas Pydantic para validação e serialização de dados.

    auth.py: Esquemas para autenticação.
    user.py: Esquemas para usuários.
    ticket.py: Esquemas para tickets.
    severity.py: Esquemas para severidades.
    subcategory.py: Esquemas para subcategorias.
    category.py: Esquemas para categorias.

Diretório scripts/

Scripts utilitários para tarefas específicas.

    checker/: Scripts para verificações de código.
        commit_check.py: Script de verificação de commits.
    external/: Scripts para integração externa.
        external.py: Integração com serviços externos.
    db_container_setup/: Scripts para configuração do banco de dados.
        container_setup.py: Configuração inicial do container de banco de dados.

Diretório api/

Definições de rotas e controladores da API.

    v1/: Primeira versão da API.
        health.py: Verificação de saúde da API.
        routers/: Definições de rotas.
            auth.py: Rotas de autenticação.
            tickets.py: Rotas de tickets.
            users.py: Rotas de usuários.
            categories.py: Rotas de categorias.
            subcategories.py: Rotas de subcategorias.
            severities.py: Rotas de severidades.
        controllers/: Lógica de negócio para cada recurso.
            severity_controller.py: Controle de severidades.
            ticket_controller.py: Controle de tickets.
            users_controller.py: Controle de usuários.
            category_controller.py: Controle de categorias.
            subcategory_controller.py: Controle de subcategorias.

Diretório infrastructure/

Configuração da infraestrutura da aplicação.

    database/: Configuração e modelos de banco de dados.
        setup.py: Configuração do banco de dados.
        base.py: Base para modelos SQLAlchemy.
        models/: Definições de modelos de dados.
            user.py: Modelo de usuário.
            ticket.py: Modelo de ticket.
            severity.py: Modelo de severidade.
            subcategory.py: Modelo de subcategoria.
            category.py: Modelo de categoria.
            ticket_category.py: Associação de tickets a categorias.
            ticket_subcategory.py: Associação de tickets a subcategorias.
```

## Métricas - Datadog e New Relic

### 1. Métricas do Painel de Controle do Datadog

#### Métricas de Desempenho da Aplicação
- **Latência de Requisição:** 
  - Medir o tempo de resposta da aplicação para as requisições de API.
  - Ajuda a identificar endpoints lentos que podem afetar a experiência do usuário.

- **Taxa de Erro:** 
  - Acompanhar a porcentagem de requisições que resultam em erros.
  - Facilita a identificação e resolução rápida de problemas na aplicação.

- **Uso de CPU e Memória:** 
  - Monitorar os recursos do sistema para garantir que a aplicação funcione de forma eficiente.
  - Evitar gargalos de desempenho.

- **Desempenho de Consultas ao Banco de Dados:** 
  - Medir o tempo de execução das consultas ao banco de dados.
  - Identificar consultas lentas que podem impactar o desempenho da aplicação.

#### Métricas de Experiência do Usuário
- **Tempo de Carregamento de Página:** 
  - Acompanhar o tempo de carregamento das páginas do ponto de vista do usuário.
  - Esta métrica ajuda a otimizar o desempenho do frontend.

- **Engajamento do Usuário:** 
  - Monitorar atividades do usuário, como o número de logins, sessões de usuários e ações realizadas.
  - Ajuda a entender como os usuários estão interagindo com a aplicação.

- **Taxa de Rejeição:** 
  - Medir a porcentagem de usuários que saem da aplicação após visualizar apenas uma página.
  - Uma alta taxa de rejeição pode indicar problemas de usabilidade ou conteúdo irrelevante.

#### Métricas de Insights para Suporte
- **Volume de Tickets:** 
  - Acompanhar o número de tickets de suporte criados ao longo do tempo.
  - Ajuda a entender a carga de trabalho da equipe de suporte e identificar horários de pico.

- **Tempo de Resolução de Tickets:** 
  - Medir o tempo médio para resolver tickets de suporte.
  - Esta métrica é crucial para avaliar a eficiência da equipe de suporte.

- **Problemas Comuns de Suporte:** 
  - Identificar os problemas mais comuns relatados pelos usuários.
  - Ajuda a priorizar correções de bugs e melhorias de funcionalidades.

- **Feedback e Avaliações de Usuários:** 
  - Coletar e analisar feedbacks e avaliações dos usuários sobre interações de suporte.
  - Medir a satisfação do usuário.

### 2. Métricas de Monitoramento do New Relic

#### Métricas de Saúde da Aplicação
- **Apdex Score:** 
  - Medir a satisfação do usuário com base nos tempos de resposta da aplicação.
  - Fornece uma visão geral do desempenho da aplicação e da experiência do usuário.

- **Rastros de Transação:** 
  - Analisar rastros de transação detalhados para identificar gargalos e otimizar o desempenho da aplicação.

- **Análise de Erros:** 
  - Monitorar taxas de erros e detalhes para identificar e resolver rapidamente problemas da aplicação.

- **Mapa de Serviços:** 
  - Visualizar a arquitetura da aplicação e as interações entre diferentes serviços.
  - Garantir operações fluidas.

#### Métricas de Infraestrutura
- **Monitoramento da Saúde do Servidor:** 
  - Acompanhar a saúde e o desempenho dos servidores que hospedam a aplicação.
  - Inclui uso de CPU, memória, disco e desempenho de rede.

- **Alertas e Notificações:** 
  - Configurar alertas para problemas críticos, como altas taxas de erro, tempos de resposta lentos ou indisponibilidades do servidor.
  - Garantir respostas e resoluções rápidas.

- **Monitoramento de Serviços em Nuvem:** 
  - Monitorar o desempenho e a disponibilidade dos serviços em nuvem utilizados pela aplicação, como bancos de dados, armazenamento e serviços de mensagens.

#### Métricas de Comportamento do Usuário
- **Rastros de Sessão:** 
  - Acompanhar sessões de usuários para analisar o comportamento do usuário.
  - Identificar funcionalidades populares e detectar possíveis problemas de usabilidade.

- **Taxas de Conversão:** 
  - Medir as taxas de conversão para ações chave na aplicação, como criação de conta ou submissão de tickets.
  - Avaliar a eficácia da jornada do usuário.

- **Análise de Caminhos do Usuário:** 
  - Analisar os caminhos comuns percorridos pelos usuários dentro da aplicação.
  - Identificar possíveis pontos de atrito e otimizar a experiência do usuário.

# Meli Ticket Management System

## Descrição do Projeto

Este projeto é uma aplicação CRUD para gerenciamento de tickets, que inclui categorias, subcategorias e severidade, além de integração com uma API externa e uso de containers Docker.

## Sprint Goal

Desenvolver uma aplicação CRUD para gerenciamento de tickets com integração de API externa e containerização usando Docker, seguindo boas práticas de desenvolvimento e documentação.

## Tecnologias Utilizadas

- Linguagem de Programação: Python
- Banco de Dados: PostgreSQL
- Containerização: Docker
- Frontend: React

## Funcionalidades

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

## Boas Práticas de Desenvolvimento

- **GitFlow**: Utilizado para gerenciamento de branches.
- **SOLID, DRY, KISS**: Princípios aplicados ao código.
- **Testes**: Testes unitários e de integração para garantir a qualidade.
- **CI/CD**: GitHub Actions para automação de builds e testes.

## Tasks

### 1. Setup do Ambiente de Desenvolvimento

- **Configurar repositório no GitHub**
  - Criar um novo repositório no GitHub para o projeto.
  - Inicializar o repositório com um arquivo README.md e .gitignore adequado.
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

1. Clone o repositório usando SSH:
   ```bash
   git clone git@github.com:oliveirakcs/ticket-management.git
   
   Nota: Certifique-se de ter uma chave SSH configurada no seu GitHub para realizar o clone via SSH.
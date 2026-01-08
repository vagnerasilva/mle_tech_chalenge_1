| ![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg) ![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688?logo=fastapi) ![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white) ![Test Coverage](https://img.shields.io/badge/test%20coverage-70%25-green.svg) ![MIT License](https://img.shields.io/badge/license-MIT-yellow.svg) |
|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|

# 📚 API Pública para Consulta de Livros – Projeto de Recomendação

## 📌 Descrição
Este projeto faz parte do Tech Challenge, cujo objetivo é aplicar de forma integrada os conhecimentos adquiridos na fase, desenvolvendo uma solução completa de dados (**web scraping** do site [Books to Scrape](https://books.toscrape.com/)), desde a coleta até a disponibilização via API pública.(FastAPI + SQLite)

O desafio consiste em criar uma API pública para consulta de livros, alimentada por dados extraídos através de um sistema automatizado de web scraping do site Books to Scrape.



- Extrair os dados brutos do site;

- Transformar e padronizar as informações coletadas;

- Armazenar esses dados localmente;

- Disponibilizar as informações através de uma API RESTful escalável e reutilizável, pronta para integração com futuros modelos de Machine Learning.

A API foi projetada pensando em flexibilidade, boa organização arquitetural e facilidade de consumo por cientistas de dados, sistemas externos e serviços de recomendação.
Com isso, este repositório reúne todos os componentes essenciais: o web scraper, a estruturação do pipeline de dados, a API pública, a documentação e o deploy em produção.

---
## 🏗️ Arquitetura
Pipeline de dados:
1. **Ingestão** → Web Scraping dos livros.  
2. **Processamento** → Transformação e armazenamento em CSV.  
3. **API** → Disponibilização dos dados via endpoints RESTful.  
4. **Consumo** → Cientistas de dados e serviços de recomendação.  

👉 [Diagrama Arquitetural link](https://drive.google.com/file/d/1mMyyxBYCTEJ7NRglnSQaWxvrKwlm-D3H/view?usp=sharing) <!-- substitua pelo seu diagrama -->

---


### 📂 Estrutura do Repositório

```
.
├── README.md
├── app
|   ├── db
│   |   └── books.db
│   ├── __init__.py
│   ├── app.py
│   ├── dependencies.py
│   ├── .env
│   ├── settings.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── book.py
│   │   ├── category.py
│   │   ├── stats.py
│   │   └── logs.py
│   ├── routers
│   │   ├── __init__.py
│   │   ├── book.py
│   │   ├── category.py
│   │   ├── health.py
│   │   ├── scraping.py
│   │   ├── stats.py
|   |   ├── callback.py
│   │   ├── home.py
│   │   ├── login.py
│   │   ├── logout.py
│   │   ├── log.py
│   │   └── nolog.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── book.py
│   │   ├── category.py
│   │   ├── scraping.py
│   │   ├── stats.py
│   │   ├── auth_middleware.py
│   │   └── log.py
│   └── utils
│       ├── __init__.py
│       └── constants.py
├── create_db.py
├── docs
│   ├── book_scraping_model.md
│   ├── db_models.md
│   ├── ddl.sql
│   ├── scraping_architecture.drawio
│   └── uml/
├── requirements.txt
└── tests
    └── readme.md
```


---

## 📡 Endpoints da API (resumo)
- GET /api/v1/books → Lista todos os livros.
- GET /api/v1/books/{id} → Detalhes de um livro específico.
- GET /api/v1/books/search?title={title}&category={category} → Busca por título/categoria.
- GET /api/v1/categories → Lista categorias disponíveis.
- GET /api/v1/health → Status da API.
- GET /api/v1/stats/overview → Estatísticas gerais.
- GET /api/v1/stats/categories → Estatísticas por categoria.
- GET /api/v1/books/top-rated → Livros com melhor avaliação.
- GET /api/v1/books/price-range?min={min}&max={max} → Livros por faixa de preço.
- GET /callback → Rota para receber a autenticação
- GET / → Rota não logada
- GET /api/v1/home → Rota para home
- GET /login → Rota para logar
- GET /api/v1/logout → Rota para sair da api
- GET /api_logs → Informações de performance e logs das chamadas de api.

## 📊 Endpoints Detalhados (Diagramas de Sequência)

Todos os endpoints possuem diagramas de sequência em `docs/uml/` descrevendo o fluxo de execução:

### Core
- [`sequence_list_books.md`](docs/uml/sequence_list_books.md) — GET /books (lista todos os livros)
- [`sequence_get_book.md`](docs/uml/sequence_get_book.md) — GET /books/{id} (livro específico)
- [`sequence_search_books.md`](docs/uml/sequence_search_books.md) — GET /books/search (busca por título/categoria)
- [`sequence_list_categories.md`](docs/uml/sequence_list_categories.md) — GET /categories (lista categorias)
- [`sequence_health.md`](docs/uml/sequence_health.md) — GET /health (status da API)

### Insights
- [`sequence_stats_overview.md`](docs/uml/sequence_stats_overview.md) — GET /stats/overview (estatísticas gerais)
- [`sequence_stats_categories.md`](docs/uml/sequence_stats_categories.md) — GET /stats/categories (estatísticas por categoria)
- [`sequence_top_rated.md`](docs/uml/sequence_top_rated.md) — GET /books/top-rated (livros melhor avaliados)
- [`sequence_price_range.md`](docs/uml/sequence_price_range.md) — GET /books/price-range (livros por faixa de preço)

### Monitoring & Logs
- [`sequence_get_api_logs.md`](docs/uml/sequence_get_api_logs.md) — GET /api_logs (consulta de logs)
- [`class_api_log.md`](docs/uml/class_api_log.md) — Diagrama de classes do modelo `ApiLog`

> Visualizações pré-geradas: `docs/uml/sequence_get_api_logs.svg`, `docs/uml/sequence_get_api_logs.png`, `docs/uml/sequence_get_api_logs.html` e `docs/uml/class_api_log.svg`, `docs/uml/class_api_log.png`, `docs/uml/class_api_log.html` — abra os `.html` para exportar as imagens via navegador.

Cada arquivo Markdown contém um diagrama Mermaid que pode ser visualizado diretamente no GitHub ou em ferramentas Mermaid.

## 🚀 Instalação rápida

```bash
git clone https://github.com/vagnerasilva/mle_tech_chalenge_1.git
cd mle_tech_chalenge_1
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate    # Windows (PowerShell)
pip install -r requirements.txt
```

---

## 🧪 Testes Unitários

A aplicação possui suite completa de testes com **66% de cobertura** de código.

### Instalação de dependências de teste
```bash
pip install -r requirements-dev.txt
```

### Executar testes
```bash
# Todos os testes
pytest tests/ -v

# Com cobertura de código
pytest tests/ --cov=app --cov-report=html

# Testes específicos
pytest tests/test_models.py -v      # Modelos (100% cobertura)
pytest tests/test_services.py -v    # Serviços (72% cobertura)
pytest tests/test_routers.py -v     # Endpoints
```

### Estrutura dos testes
- **test_models.py** (10 testes): Validação de modelos SQLAlchemy e schemas Pydantic
- **test_services.py** (18 testes): Testes da lógica de negócio (book, category, stats services)
- **test_routers.py** (6 testes): Testes de endpoints públicos (requer configuração adicional para endpoints autenticados)
- **conftest.py**: Fixtures reutilizáveis (DB mock, TestClient, dados de teste)

📖 [Documentação detalhada](tests/README.md)

---

---

## 📌 Roadmap da execuçäo Projeto pelo time

Este documento apresenta o planejamento do projeto em formato **roadmap**, dividido em sprints de 3 semanas, com visão estilo **Gantt** e **heatmap visual** para destacar dependências entre tarefas. Bem tb como o Trello de acompanhamento da evolucao do projeto.

---


## 📊 Roadmap por Semana – Projeto API Pública para Consulta de Livros

| Tarefa                          | Semana 1 | Semana 2 | Semana 3 | Semana 4 | Semana 5 | Semana 6 |
|---------------------------------|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|
| Setup & Scraping                | 🟩🟩🟩     |          |          |          |          |          |
| API Core                        |          | → 🟦🟦🟦   |          |          |          |          |
| Deploy & Arquitetura            |          |          | → 🟨🟨🟨   |          |          |          |
| Insights & Estatísticas         |          |          |          | → 🟪🟪🟪   |          |          |
| Bônus & ML-ready                |          |          |          |          | → 🟥🟥🟥   |          |
| Finalização & Apresentação      |          |          |          |          |          | → 🟧🟧🟧   |

---

## 🎨 Legenda de cores
- 🟩 Setup & Scraping  
- 🟦 API Core  
- 🟨 Deploy & Arquitetura  
- 🟪 Insights & Estatísticas  
- 🟥 Bônus & ML-ready  
- 🟧 Finalização & Apresentação  


- [Trello de evolucao do projeto](https://trello.com/b/7Lrv480a/tech-chalenge-i)
---

## 📌 Observações


A aplicação possui uma suíte de testes. Execute `pytest tests/` localmente para ver o estado atual dos testes e consulte `tests/readme.md` para informações sobre cobertura e relatórios (HTML).

**Relatório HTML de cobertura:** [tests/htmlcov/index.html](tests/htmlcov/index.html)
    - Abra esse arquivo localmente no seu navegador para visualização interativa.

### Pré-requisitos
- Python 3.9+
- Pip ou Poetry
- Conta em render.com

### Passos
bash
# Clonar repositório
```bash
git clone https://github.com/vagnerasilva/mle_tech_chalenge_1.git
cd seu-repo
```
# Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```


# Instalar dependências
```bash
pip install -r requirements.txt
```


# Executar scraping
```bash
# Execute o módulo de scraping (do diretório raiz do projeto)
python -m app.services.scraping
```

# Rodar API localmente
```bash
# Inicie o servidor de desenvolvimento
uvicorn app.app:app --reload
# Inicie o servidor de desenvolvimento em prod ( render)
uvicorn app.app:app --host 0.0.0.0 --port 10000 --reload
```

´´´



## 📡 Endpoints da API
- Core

GET /api/v1/books → Lista todos os livros.

GET /api/v1/books/{id} → Detalhes de um livro específico.

GET /api/v1/books/search?title={title}&category={category} → Busca por título/categoria.

GET /api/v1/categories → Lista categorias disponíveis.

GET /api/v1/health → Status da API.

## Insights (opcionais)

GET /api/v1/stats/overview → Estatísticas gerais.

GET /api/v1/stats/categories → Estatísticas por categoria.

GET /api/v1/books/top-rated → Livros com melhor avaliação.

GET /api/v1/books/price-range?min={min}&max={max} → Livros por faixa de preço.

## ML-ready (bônus)

*Observação: esses endpoints são planejados e **não** estão implementados atualmente.*

- GET /api/v1/ml/features → Dados formatados para features. (planejado)
- GET /api/v1/ml/training-data → Dataset para treinamento. (planejado)
- POST /api/v1/ml/predictions → Endpoint para predições. (planejado)

## Monitoramento & Analytics (bônus)

GET /api_logs → Informações de performance e logs das chamadas de api.

# 🌐 Deploy
A API está disponível publicamente em: 

👉 [https://mle-tech-chalenge-1.onrender.com/](https://mle-tech-chalenge-1.onrender.com/)


# 🎥 Vídeo de Apresentação
👉 Link do Vídeo




# 📑 Plano de Integração com Modelos de Machine Learning
## Objetivo
Este plano descreve como a API pública de livros será integrada com modelos de Machine Learning (ML), garantindo que os dados coletados via web scraping sejam disponibilizados de forma escalável, reutilizável e prontos para consumo em sistemas de recomendação, análise estatística e predição.

## Fluxo de Integração com ML

### Ingestão de Dados

Cientistas de dados acessam /api/v1/ml/training-data para obter as bases de dados em formato JSON para treinamento.

### Análise dos dados

Cientistad de dados usam /api/v1/stats/overview e /api/v1/stats/categories para analisar a distribuição dos dados por rating ou por categoria.
 
### Preparação de Features

Endpoint /api/v1/ml/features fornece dados já normalizados, facilitando integração direta com frameworks como Scikit-learn, TensorFlow ou PyTorch.

### Treinamento de Modelos

Modelos de recomendação são treinados usando os dados obtidos por requisições e armazenados em catalogos de modelos para versionamento dos modelos.

### Deploy de Modelos

Modelos são expostos como serviços via FastAPI através do endpoint /api/v1/ml/predictions.

### Consumo de Predições

Aplicações externas chamam /api/v1/ml/predictions enviando dados de entrada. API retorna recomendações personalizadas ou insights.

## Cenários de Uso
- Recomendação de Livros  
Usuário consulta /api/v1/ml/predictions e recebe sugestões baseadas em categoria e rating.

- Treinamento de Modelos de Classificação  
Cientistas de dados usam /api/v1/ml/training-data para treinar modelos que classificam livros por popularidade ou faixa de preço.

- Dashboards Analíticos  
Dados de /api/v1/stats/* podem ser integrados em ferramentas como Streamlit para visualização.

## Escalabilidade e Futuro
- Banco de Dados: migrar para soluções escaláveis (PostgreSQL + Redis para cache).

- Pipeline de Dados: orquestração com Airflow por exemplo.

- Modelos ML: deploy em nuvem (Google Vertex AI, AWS Sagemaker).

- Monitoramento: logs estruturados + métricas de performance expostas em Streamlit/Grafana.

## Diagrama Visual

```mermaid
flowchart TD
  A[Web Scraping] --> B[Processing]
  B --> C[Database]
  C --> D[API REST<br>/books /categories<br>/ml/features<br>/ml/training-data<br>/ml/predictions]
  D --> E[ML Model<br>(Recommender System)]
  E --> F[Consumers/Apps]
```



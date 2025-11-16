| ![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg) ![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688?logo=fastapi) ![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white) ![MIT License](https://img.shields.io/badge/license-MIT-yellow.svg) |
|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|

# 📚 API Pública para Consulta de Livros – Projeto de Recomendação

## 📌 Descrição
Este projeto faz parte do Tech Challenge, cujo objetivo é aplicar de forma integrada os conhecimentos adquiridos na fase, desenvolvendo uma solução completa de dados (**web scraping** do site [Books to Scrape](https://books.toscrape.com/)), desde a coleta até a disponibilização via API pública.

O desafio consiste em criar uma API pública para consulta de livros, alimentada por dados extraídos através de um sistema automatizado de web scraping do site Books to Scrape.

Como Engenheiro(a) de Machine Learning no contexto do projeto, o primeiro passo é estruturar um pipeline capaz de:

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

![Diagrama Arquitetural](docs/arquitetura.png) <!-- substitua pelo seu diagrama -->

---
### 📂 Estrutura do Repositório

```
.
├── README.md
├── api
│   └── readme.md
├── app
│   ├── __init__.py
│   ├── app.py
│   ├── dependencies.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── book.py
│   │   ├── category.py
│   │   └── stats.py
│   ├── routers
│   │   ├── __init__.py
│   │   ├── book.py
│   │   ├── category.py
│   │   ├── health.py
│   │   ├── scraping.py
│   │   └── stats.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── book.py
│   │   ├── category.py
│   │   ├── scraping.py
│   │   └── stats.py
│   └── utils
│       ├── __init__.py
│       └── constants.py
├── create_db.py
├── db
│   ├── book_scraping_model
│   │   ├── __init__.py
│   │   ├── book.py
│   │   └── category.py
│   └── books.db
├── docs
│   ├── arquivo.txt
│   ├── book_scraping_model.md
│   ├── readme.md
│   └── requirements.txt
├── requirements.txt
└── tests
    └── readme.md
```

## 📌 Roadmap da execuçäo Projeto – API Pública para Consulta de Livros

Este documento apresenta o planejamento do projeto em formato **roadmap**, dividido em sprints de 3 semanas, com visão estilo **Gantt** e **heatmap visual** para destacar dependências entre tarefas.

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


- [Trello](https://trello.com/b/7Lrv480a/tech-chalenge-i)
---

## 📌 Observações
- Cada etapa depende da anterior (ex.: API Core só começa após Scraping).  
- O roadmap foi pensado para **entregas incrementais**: MVP na Sprint 1 e funcionalidades avançadas na Sprint 2.  
- Este documento deve ser usado em conjunto com o **Kanban detalhado** para acompanhamento micro das tarefas.  


# 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.9+
- Pip ou Poetry
- Conta em Heroku/Render/Fly.io (para deploy)

### Passos
bash
# Clonar repositório
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar scraping
python scripts/scraping.py

# Rodar API localmente
uvicorn api.main:app --reload
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
GET /api/v1/ml/features → Dados formatados para features.

GET /api/v1/ml/training-data → Dataset para treinamento.

POST /api/v1/ml/predictions → Endpoint para predições.


# 🌐 Deploy
A API está disponível publicamente em: 👉 Link do Deploy

# 🎥 Vídeo de Apresentação
👉 Link do Vídeo




📜 Licença
Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.



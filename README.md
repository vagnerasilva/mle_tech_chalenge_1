# 📌 Roadmap do Projeto – API de Livros

Este documento apresenta o planejamento do projeto em formato **roadmap**, dividido em sprints de 3 semanas, com visão estilo **Gantt** e **heatmap visual** para destacar dependências entre tarefas.

---

## 📅 Roadmap por Semana – Projeto API de Livros

Legenda:
- █ = execução da tarefa
- → = dependência (só começa após a anterior)

Semanas:   1     2     3     4     5     6
----------------------------------------------
Setup & Scraping       █████
API Core                     → █████
Deploy & Arquitetura                → █████
Insights & Estatísticas                   → █████
Bônus & ML-ready                               → █████
Finalização & Apresentação                          → █████

---

## 📊 Roadmap por Semana – Projeto API de Livros

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

---

## 📌 Observações
- Cada etapa depende da anterior (ex.: API Core só começa após Scraping).  
- O roadmap foi pensado para **entregas incrementais**: MVP na Sprint 1 e funcionalidades avançadas na Sprint 2.  
- Este documento deve ser usado em conjunto com o **Kanban detalhado** para acompanhamento micro das tarefas.  


# 📚 API Pública de Livros – Projeto de Recomendação

## 📌 Descrição
Este projeto tem como objetivo criar uma **API pública para consulta de livros**, utilizando dados extraídos via **web scraping** do site [Books to Scrape](https://books.toscrape.com/).  
A API foi pensada para ser **escalável, reutilizável e pronta para integração com modelos de Machine Learning**.

---

## 🏗️ Arquitetura
Pipeline de dados:
1. **Ingestão** → Web Scraping dos livros.  
2. **Processamento** → Transformação e armazenamento em CSV.  
3. **API** → Disponibilização dos dados via endpoints RESTful.  
4. **Consumo** → Cientistas de dados e serviços de recomendação.  

![Diagrama Arquitetural](docs/arquitetura.png) <!-- substitua pelo seu diagrama -->

---

## 🚀 Instalação e Configuração

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



📡 Endpoints da API
Core
GET /api/v1/books → Lista todos os livros.

GET /api/v1/books/{id} → Detalhes de um livro específico.

GET /api/v1/books/search?title={title}&category={category} → Busca por título/categoria.

GET /api/v1/categories → Lista categorias disponíveis.

GET /api/v1/health → Status da API.

Insights (opcionais)
GET /api/v1/stats/overview → Estatísticas gerais.

GET /api/v1/stats/categories → Estatísticas por categoria.

GET /api/v1/books/top-rated → Livros com melhor avaliação.

GET /api/v1/books/price-range?min={min}&max={max} → Livros por faixa de preço.

ML-ready (bônus)
GET /api/v1/ml/features → Dados formatados para features.

GET /api/v1/ml/training-data → Dataset para treinamento.

POST /api/v1/ml/predictions → Endpoint para predições.

📅 Roadmap
Confira o planejamento completo em ROADMAP.md. Resumo das sprints:

Sprint 1 (Semanas 1–3): Scraping + API Core + Deploy.

Sprint 2 (Semanas 4–6): Insights + ML-ready + Autenticação + Apresentação.

🌐 Deploy
A API está disponível publicamente em: 👉 Link do Deploy

🎥 Vídeo de Apresentação
👉 Link do Vídeo

👨‍💻 Contribuição
Faça um fork do projeto.

Crie uma branch (feature/nova-feature).

Commit suas alterações.

Abra um Pull Request.

📜 Licença
Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.



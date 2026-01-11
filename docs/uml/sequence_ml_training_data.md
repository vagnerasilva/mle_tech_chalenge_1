# Diagrama de Sequência: GET /api/v1/ml/training-data

## Fluxo de Execução

```mermaid
sequenceDiagram
    participant Client
    participant FastAPI as FastAPI Router
    participant MLService as ML Service
    participant Database as Database
    participant Response

    Client->>FastAPI: GET /api/v1/ml/training-data?limit=500
    activate FastAPI
    
    Note over FastAPI: Valida parâmetros<br/>(limit: int, opcional)
    
    FastAPI->>MLService: get_training_data(db, limit=500)
    activate MLService
    
    Note over MLService: Prepara query com JOIN<br/>Books + Categories<br/>com LIMIT opcional
    
    MLService->>Database: SELECT * FROM books<br/>JOIN categories<br/>WHERE ... LIMIT 500
    activate Database
    
    Database-->>MLService: Lista completa de livros
    deactivate Database
    
    Note over MLService: Para cada livro:<br/>- Extrai todos os campos<br/>- Inclui dados de categoria<br/>- Cria TrainingData object
    
    MLService->>Database: SELECT COUNT(DISTINCT category_id)
    activate Database
    Database-->>MLService: Total de categorias
    deactivate Database
    
    MLService->>MLService: Calcula estatísticas completas:<br/>- Distribuição de ratings<br/>- Distribuição de preços<br/>- Categorias/Tipos únicos
    
    MLService-->>FastAPI: Dict com dataset + stats
    deactivate MLService
    
    Note over FastAPI: Valida resposta<br/>com MLDatasetResponse (Pydantic)
    
    FastAPI->>Response: JSON 200 OK
    activate Response
    
    Response-->>Client: {<br/>  "total_records": 500,<br/>  "total_categories": 5,<br/>  "data": [...],<br/>  "statistics": {...}<br/>}
    deactivate Response
    
    deactivate FastAPI
```

## Detalhes do Endpoint

- **Rota:** `GET /api/v1/ml/training-data`
- **Descrição:** Retorna dataset completo para treinamento de modelos
- **Query Parameters:**
  - `limit` (opcional, int): Limita quantidade de registros
- **Status Code:** 200 OK
- **Modelo de Resposta:** `MLDatasetResponse`

## Campos do Dataset

```
Dados Básicos:
- book_id: Identificador único
- title: Título do livro
- description: Descrição completa
- product_type: Tipo de produto (Hardcover, Paperback, etc)

Dados Financeiros:
- price_excl_tax: Preço sem imposto
- price_incl_tax: Preço com imposto
- tax: Valor do imposto

Dados de Avaliação:
- rating: Avaliação (0-5)
- number_of_reviews: Número de avaliações

Dados de Inventário:
- availability: Quantidade disponível
- upc: Universal Product Code

Dados de Categorização:
- category_id: ID da categoria
- category_name: Nome da categoria
- image_url: URL da imagem
```

## Estatísticas Incluídas

```json
{
  "rating_distribution": {
    "avg": 3.8,
    "min": 1,
    "max": 5
  },
  "price_distribution": {
    "avg": 25.50,
    "min": 5.99,
    "max": 89.99
  },
  "reviews_avg": 120,
  "unique_categories": 5,
  "unique_product_types": 3
}
```

## Exemplo de Resposta Parcial

```json
{
  "total_records": 500,
  "total_categories": 5,
  "data": [
    {
      "book_id": 1,
      "title": "The Great Gatsby",
      "description": "A classic novel about...",
      "product_type": "Hardcover",
      "price_excl_tax": 25.00,
      "price_incl_tax": 29.99,
      "tax": 4.99,
      "availability": 50,
      "number_of_reviews": 150,
      "upc": "9780123456789",
      "rating": 4,
      "category_id": 1,
      "category_name": "Fiction",
      "image_url": "https://example.com/image.jpg"
    }
  ],
  "statistics": {
    "rating_distribution": {"avg": 3.8, "min": 1, "max": 5},
    "price_distribution": {"avg": 25.50, "min": 5.99, "max": 89.99},
    "reviews_avg": 120,
    "unique_categories": 5,
    "unique_product_types": 3
  }
}
```

## Caso de Uso

Cientista de dados obtém dataset completo para:
- Treinar modelos de recomendação
- Análise exploratória e estatística
- Validação de hipóteses
- Criação de features customizadas

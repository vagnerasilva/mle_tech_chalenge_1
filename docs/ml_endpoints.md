# Endpoints de ML - Documentação

## Visão Geral
Conjunto de endpoints desenvolvidos para facilitar o consumo de modelos de Machine Learning. Estes endpoints fornecem dados estruturados para treinamento, features normalizadas para predição e recebimento de resultados de modelos.

## Endpoints Disponíveis

### 1. GET `/api/v1/ml/features`
**Descrição:** Retorna features normalizadas para consumo de modelos ML.

**Query Parameters:**
- `limit` (opcional, int): Limite de registros a retornar. Se não informado, retorna todos.

**Resposta (200 OK):**
```json
{
  "total_records": 100,
  "features": [
    {
      "book_id": 1,
      "title": "Book Title",
      "rating": 0.8,
      "price": 29.99,
      "availability": 50,
      "number_of_reviews": 150,
      "category_id": 1,
      "category_name": "Fiction",
      "description_length": 500
    }
  ],
  "feature_names": [
    "book_id",
    "rating",
    "price",
    "availability",
    "number_of_reviews",
    "category_id",
    "description_length"
  ],
  "statistics": {
    "rating_avg": 0.75,
    "rating_min": 0.2,
    "rating_max": 1.0,
    "price_avg": 25.50,
    "price_min": 5.99,
    "price_max": 89.99,
    "reviews_avg": 120,
    "availability_avg": 40
  }
}
```

**Features Normalizadas:**
- `rating`: Normalizado entre 0-1 (original 0-5)
- `price`: Preço inclusivo de imposto
- `availability`: Quantidade em estoque
- `description_length`: Tamanho em caracteres da descrição

**Uso:** Ideal para treinamento de modelos de recomendação, classificação e predição de ratings.

---

### 2. GET `/api/v1/ml/training-data`
**Descrição:** Retorna dataset completo para treinamento de modelos ML.

**Query Parameters:**
- `limit` (opcional, int): Limite de registros a retornar. Se não informado, retorna todos.

**Resposta (200 OK):**
```json
{
  "total_records": 100,
  "total_categories": 5,
  "data": [
    {
      "book_id": 1,
      "title": "Book Title",
      "description": "Full book description...",
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
}
```

**Informações Incluídas:**
- Dados completos do livro (descrição, preços, avaliações)
- Metadados (UPC, tipo de produto, URL da imagem)
- Informações de categoria
- Disponibilidade e número de reviews

**Estatísticas Incluídas:**
- Distribuição de ratings
- Distribuição de preços
- Média de reviews
- Número de categorias únicas
- Número de tipos de produtos únicos

**Uso:** Ideal para treinamento completo de modelos com todos os dados históricos.

---

### 3. POST `/api/v1/ml/predictions`
**Descrição:** Recebe e processa predições de modelos ML.

**Request Body:**
```json
{
  "features": {
    "rating": 4.5,
    "price": 29.99,
    "number_of_reviews": 150,
    "category_id": 1,
    "availability": 50
  },
}
```

**Resposta (200 OK):**
```json
{
  "prediction": {
    "rating": 0.9,
    "price": 29.99,
    "number_of_reviews": 150,
    "category_id": 1,
    "availability": 50
  },
  "confidence": 0.85,
  "message": "Predição do tipo 'recommendation' recebida e processada com sucesso"
}
```

**Processamento Realizado:**
- Normalização de features (ex: rating 0-5 → 0-1)
- Validação de dados de entrada
- Armazenamento de log da predição

**Erros Possíveis:**
- `400 Bad Request`: Dados de entrada inválidos
- `500 Internal Server Error`: Erro ao processar predição

**Uso:** Endpoint para consumir resultados de modelos ML externos ou integrados, com validação e logging automático.

---

## Exemplo de Fluxo Completo

### 1. Obter Features para Treinamento
```bash
curl -X GET "http://localhost:8000/api/v1/ml/features?limit=100" \
  -H "accept: application/json"
```

### 2. Obter Dataset Completo
```bash
curl -X GET "http://localhost:8000/api/v1/ml/training-data?limit=500" \
  -H "accept: application/json"
```

### 3. Enviar Predição
```bash
curl -X POST "http://localhost:8000/api/v1/ml/predictions" \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "rating": 4.5,
      "price": 29.99,
      "number_of_reviews": 150,
      "category_id": 1
    },
    "model_type": "recommendation"
  }'
```

---

## Autenticação
Por padrão, estes endpoints podem estar protegidos por autenticação baseada em sessão. Consulte a documentação de autenticação da API para mais detalhes.

---

## Performance
- **Features**: Otimizado com índices de banco de dados
- **Training Data**: Pode retornar grande volume de dados; considere usar `limit` para dados maiores
- **Predictions**: Processamento assíncrono com logging em background

---

## Estrutura de Normalização
As features são normalizadas conforme segue:
- **Rating**: Dividido por 5.0 (0-5 → 0-1)
- **Price**: Mantido como está (em unidade monetária)
- **Availability**: Quantidade inteira
- **Description Length**: Tamanho em caracteres

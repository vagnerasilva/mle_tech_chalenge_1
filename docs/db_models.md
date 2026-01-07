# Documentação Técnica — Banco de Dados e Modelos (SQLite)

Este documento descreve o modelo relacional usado pelo projeto, os schemas Pydantic usados para validação/serialização e exemplos de inserção/consultas. Os artefatos de modelagem estão em `app/models/`.

## Visão geral

- Banco: SQLite
- Arquivo DB: `app/db/books.db`
- Engine SQLAlchemy: `create_engine("sqlite:///app/db/books.db", connect_args={"check_same_thread": False})`
- Sessões: `SessionLocal = sessionmaker(...)` (ver `app/models/base.py`).

## Tabelas principais

### `categories`

- Nome da tabela: `categories`
- Campos:
  - `id` INTEGER PRIMARY KEY AUTOINCREMENT
  - `name` TEXT NOT NULL UNIQUE

Descrição: armazena as categorias dos livros. `name` é único para evitar duplicatas.

Exemplo SQL CREATE (aproximado):

```sql
CREATE TABLE categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);
```

### `books`

- Nome da tabela: `books`
- Campos (mapeados a partir de `app/models/book.py`):
  - `id` INTEGER PRIMARY KEY AUTOINCREMENT
  - `title` TEXT NOT NULL
  - `description` TEXT NOT NULL
  - `product_type` TEXT NOT NULL
  - `price_excl_tax` REAL NOT NULL
  - `price_incl_tax` REAL NOT NULL
  - `tax` REAL NOT NULL
  - `availability` INTEGER NOT NULL
  - `number_of_reviews` INTEGER DEFAULT 0
  - `upc` TEXT NOT NULL UNIQUE
  - `rating` INTEGER -- CHECK (rating BETWEEN 0 AND 5)
  - `image_url` TEXT NOT NULL
  - `category_id` INTEGER NOT NULL REFERENCES categories(id)

Observações:
- `upc` é único (evita inserir o mesmo livro duas vezes).
- `rating` tem constraint para valores entre 0 e 5 (definida no modelo SQLAlchemy com `CheckConstraint`).
- Não há índices adicionais definidos por código além das chaves primária/única; você pode adicionar índices para consultas frequentes (ex.: `CREATE INDEX idx_books_rating ON books(rating);`).

Exemplo SQL CREATE (aproximado):

```sql
CREATE TABLE books (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  product_type TEXT NOT NULL,
  price_excl_tax REAL NOT NULL,
  price_incl_tax REAL NOT NULL,
  tax REAL NOT NULL,
  availability INTEGER NOT NULL,
  number_of_reviews INTEGER DEFAULT 0,
  upc TEXT NOT NULL UNIQUE,
  rating INTEGER,
  image_url TEXT NOT NULL,
  category_id INTEGER NOT NULL,
  FOREIGN KEY(category_id) REFERENCES categories(id)
);
-- Constraint adicional (exemplo):
-- ALTER TABLE books ADD CHECK (rating BETWEEN 0 AND 5);
```

### `api_logs`

- **Nome da tabela:** `api_logs`  
- **Campos:**
  - `id INTEGER PRIMARY KEY AUTOINCREMENT`
  - `api_key UUID (nullable)`
  - `ip_address TEXT NOT NULL`
  - `path TEXT NOT NULL`
  - `method TEXT NOT NULL`
  - `status_code INTEGER NOT NULL`
  - `request_body JSON`
  - `response_body JSON`
  - `query_params JSON`
  - `path_params JSON`
  - `process_time REAL NOT NULL`
  - `created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP`

**Descrição:** armazena logs de requisições HTTP feitas à API, incluindo informações de entrada, saída e tempo de processamento.

**Exemplo SQL CREATE:**
```sql
CREATE TABLE api_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  api_key UUID,
  ip_address TEXT NOT NULL,
  path TEXT NOT NULL,
  method TEXT NOT NULL,
  status_code INTEGER NOT NULL,
  request_body JSON,
  response_body JSON,
  query_params JSON,
  path_params JSON,
  process_time REAL NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

## Schemas Pydantic

Os arquivos `app/models/*.py` também expõem schemas para serialização/response via FastAPI.

- `BookSchema` (em `app/models/book.py`): campos correspondentes ao modelo `Book` — usado como `response_model` em endpoints. Tem `Config.from_attributes = True` para permitir conversão de objetos SQLAlchemy.

- `CategorySchema` (em `app/models/category.py`): `id`, `name`.

- `BookOverviewSchema`, `CategoryOverviewSchema` (em `app/models/stats.py`): usados para endpoints de estatísticas.

Esses schemas definem o contrato JSON retornado pela API.

## Fluxos de inserção de dados

O principal fluxo de inserção ocorre via scraping e a função `post_books` em `app/services/book.py`:

Resumo da função `post_books(books_infos: List[dict], db: Session) -> None`:

1. Para cada `book` no `books_infos` (dicionário):
   - Converte o campo `category` (nome) para `category_id` chamando `category.get_category_id_by_name(book['category'], db)` — função em `app/services/category.py` que busca/insere categoria.
   - Remove a chave `category` do dicionário e seta `category_id`.
   - Verifica se já existe um registro com o mesmo `upc` usando `db.query(Book).filter_by(upc=book['upc']).first()`; se existir, ignora a inserção deste livro.
   - Caso contrário, cria `Book(**book)` e adiciona via `db.add()`.
2. Ao final do loop, chama `db.commit()` para persistir as alterações.

Consequências importantes:
- A responsabilidade de mapear categoria para `category_id` é do serviço `category`.
- A lógica evita duplicatas por `upc` mas não faz deduplicação por título ou outros campos.

Exemplo de payload JSON para inserir um livro (estrutura esperada por `post_books` após o scraping):

```json
{
  "title": "A Light in the Attic",
  "description": "Poetry for children...",
  "product_type": "Book",
  "price_excl_tax": 51.77,
  "price_incl_tax": 54.00,
  "tax": 2.23,
  "availability": 22,
  "number_of_reviews": 0,
  "upc": "a1234567890",
  "rating": 3,
  "image_url": "http://.../image.jpg",
  "category": "Poetry"
}
```

Após o mapeamento interno, o registro persistido terá `category_id` em vez de `category`.

## Consultas comuns e exemplos SQL

- Buscar livro por id (implementado por `get_book`):
```sql
SELECT * FROM books WHERE id = :book_id;
```

- Listar livros entre faixa de preço (implementado por `get_books_between_prices`):
```sql
SELECT * FROM books WHERE price_incl_tax >= :min AND price_incl_tax <= :max;
```

- Buscar por título aproximado ou por categoria (implementado em `filter_books`):
```sql
-- filtrar por título (case-insensitive)
SELECT * FROM books WHERE title LIKE '%' || :title || '%';

-- filtrar por categoria (join)
SELECT b.* FROM books b
JOIN categories c ON b.category_id = c.id
WHERE c.name = :category;
```

- Retornar top-rated (implementado por `get_best_book`): ordenar por `rating DESC` e limitar a N resultados.
```sql
SELECT * FROM books ORDER BY rating DESC LIMIT :quant;
```

## Inspeção do banco localmente

Para inspecionar o arquivo SQLite localmente:

```bash
# usar o sqlite3 (instale se necessário)
sqlite3 app/db/books.db
# dentro do sqlite3:
.tables
PRAGMA table_info(books);
SELECT * FROM books LIMIT 10;
```


Arquivo(s) de referência do modelo

- `app/models/book.py`
- `app/models/category.py`
- `app/models/stats.py`
- `app/models/logs.py`
- `app/services/book.py` (fluxo de inserção `post_books`)
- `app/services/category.py` (mapeamento de nome -> id)



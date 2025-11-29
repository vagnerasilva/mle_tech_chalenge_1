-- DDL para SQLite gerado a partir dos modelos em app/models
-- Arquivo: docs/ddl.sql

PRAGMA foreign_keys = ON;

-- Tabela de categorias
CREATE TABLE IF NOT EXISTS categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

-- Tabela de livros
CREATE TABLE IF NOT EXISTS books (
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
  rating INTEGER CHECK(rating BETWEEN 0 AND 5),
  image_url TEXT NOT NULL,
  category_id INTEGER NOT NULL,
  FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Índices recomendados (opcionais)
-- CREATE INDEX idx_books_rating ON books(rating);
-- CREATE INDEX idx_books_price_incl_tax ON books(price_incl_tax);
-- CREATE INDEX idx_books_category_id ON books(category_id);

-- Observações:
-- - A constraint de rating foi incluída conforme definida no modelo SQLAlchemy.
-- - O campo upc foi marcado como UNIQUE para evitar duplicação de livros.
-- - Para controle de versão do esquema, recomenda-se usar Alembic em projetos maiores.

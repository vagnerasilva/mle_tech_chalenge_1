# 🗂 **Estrutura do Módulo**

```
db/
 └─ book_scraping_model/
     ├── __init__.py
     ├── book.py
     └── category.py
```

* **`__init__.py`** → inicializa o objeto `db` e o módulo
* **`book.py`** → define o modelo `Book`
* **`category.py`** → define o modelo `Category`

---

# 📚 **1. Modelo `Category`**

Representa a categoria de um livro (ex.: Travel, Fiction, Non-Fiction, etc.).

### **📄 Arquivo: `category.py`**

```python
from book_scraping_model import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
```

### **Descrição dos Campos**

| Campo  | Tipo    | Restrições       | Descrição                        |
| ------ | ------- | ---------------- | -------------------------------- |
| `id`   | Integer | PK               | Identificador único da categoria |
| `name` | Text    | Unique, Not Null | Nome da categoria                |

---

# 📘 **2. Modelo `Book`**

Representa cada livro extraído do site.

### **📄 Arquivo: `book.py`**

```python
from book_scraping_model import db
from .category import Category

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    product_type = db.Column(db.Text, nullable=False)

    price_ex_tax = db.Column(db.Float, nullable=False)
    price_inc_tax = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)

    availability = db.Column(
        db.Integer,
        db.CheckConstraint("availability IN (0, 1)"),
        nullable=False
    )

    num_reviews = db.Column(db.Integer, default=0)

    upc = db.Column(db.Text, unique=True, nullable=False)

    rate = db.Column(
        db.Integer,
        db.CheckConstraint("rate BETWEEN 0 AND 5")
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    category = db.relationship("Category", backref="books")
```

---

# 📝 **Descrição dos Campos**

### **Identificação**

| Campo | Tipo    | Restrições        | Descrição                    |
| ----- | ------- | ----------------- | ---------------------------- |
| `id`  | Integer | PK, Autoincrement | Identificador único do livro |
| `upc` | Text    | Unique, Not Null  | Código único do livro        |

---

### **Informações Gerais**

| Campo          | Tipo | Restrições | Descrição                 |
| -------------- | ---- | ---------- | ------------------------- |
| `title`        | Text | Not Null   | Título do livro           |
| `description`  | Text | Not Null   | Descrição completa        |
| `product_type` | Text | Not Null   | Tipo do produto (do site) |

---

### **Preços**

| Campo           | Tipo  | Restrições | Descrição                 |
| --------------- | ----- | ---------- | ------------------------- |
| `price_ex_tax`  | Float | Not Null   | Preço sem impostos        |
| `price_inc_tax` | Float | Not Null   | Preço com impostos        |
| `tax`           | Float | Not Null   | Valor do imposto aplicado |

---

### **Disponibilidade**

| Campo          | Tipo    | Restrições               | Descrição                         |
| -------------- | ------- | ------------------------ | --------------------------------- |
| `availability` | Integer | Not Null, Check (0 ou 1) | 0 = Indisponível / 1 = Disponível |
| `num_reviews`  | Integer | Default 0                | Número de reviews                 |
| `rate`         | Integer | Check (0 a 5)            | Avaliação do livro                |

---

### **Relacionamento**

| Campo         | Relacionamento       | Descrição                     |
| ------------- | -------------------- | ----------------------------- |
| `category_id` | FK → `categories.id` | Categoria do livro            |
| `category`    | `.relationship()`    | Objeto da categoria associada |

---

# 🔗 **Relacionamento Book ↔ Category**

### Tipo: **One-to-Many**

* **Categoria** → possui vários **Books**
* **Book** → pertence a uma única **Categoria**

### Atributos criados automaticamente:

* Para Book:

  ```python
  book.category
  ```
* Para Category:

  ```python
  category.books   # lista de todos os books da categoria
  ```

---

# 🧪 **Exemplos de Uso**

### Criar uma categoria

```python
c = Category(name="Science Fiction")
db.session.add(c)
db.session.commit()
```

---

### Criar um livro associado à categoria

```python
b = Book(
    title="Dune",
    description="A sci-fi classic",
    product_type="Book",
    price_ex_tax=40.0,
    price_inc_tax=45.0,
    tax=5.0,
    availability=1,
    upc="1234567890ABC",
    rate=5,
    category_id=c.id
)

db.session.add(b)
db.session.commit()
```

---

# 🏗 **Criação das Tabelas**

Caso necessário:

```python
from book_scraping_model import db
db.create_all()
```

---

# 🔒 **Constraints Implementadas**

| Tipo        | Campo        | Regra                                      |
| ----------- | ------------ | ------------------------------------------ |
| Unique      | upc          | Não pode haver dois livros com o mesmo UPC |
| Default     | num_reviews  | 0                                          |
| Check       | availability | 0 ou 1                                     |
| Check       | rate         | Valor entre 0 e 5                          |
| Foreign Key | category_id  | Referencia categories.id                   |

---

# 🚀 **Resumo**

O módulo book_scraping_model foi estruturado para:

✔ armazenar dados do scraping de forma organizada
✔ garantir integridade referencial
✔ validar valores com constraints
✔ facilitar consultas com relationships
✔ permitir expansão futura (Reviews, Autores, etc.)

---

Se quiser, posso gerar:

✨ **Diagrama ER (PDF ou imagem)**
✨ **README com instruções de instalação**
✨ **Versão em inglês dessa documentação**

Só pedir!

"""
conftest.py — Fixtures compartilhadas para testes unitários.
Configuração de DB mockado, cliente FastAPI e dados de teste.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient
from app.app import app
from app.models.base import Base
from app.dependencies import get_db


# DB em memória para testes
@pytest.fixture(scope="function")
def test_db():
    """Cria um banco de dados SQLite em memória para cada teste."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)


# Override de dependência para usar DB de teste
@pytest.fixture
def client(test_db: Session):
    """Retorna cliente FastAPI com DB mockado."""
    def override_get_db():
        return test_db
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


# Fixture para dados de teste (Category)
@pytest.fixture
def sample_category(test_db: Session):
    """Cria uma categoria de teste."""
    from app.models.category import Category
    
    category = Category(id=1, name="Fiction")
    test_db.add(category)
    test_db.commit()
    test_db.refresh(category)
    return category


# Fixture para dados de teste (Book)
@pytest.fixture
def sample_book(test_db: Session, sample_category):
    """Cria um livro de teste."""
    from app.models.book import Book
    
    book = Book(
        id=1,
        title="Test Book",
        description="A test book description",
        product_type="Book",
        price_excl_tax=10.50,
        price_incl_tax=12.50,
        tax=2.00,
        availability=5,
        number_of_reviews=3,
        upc="test-upc-001",
        rating=4,
        image_url="http://example.com/image.jpg",
        category_id=sample_category.id,
    )
    test_db.add(book)
    test_db.commit()
    test_db.refresh(book)
    return book


# Fixture para múltiplos livros
@pytest.fixture
def multiple_books(test_db: Session, sample_category):
    """Cria múltiplos livros para testes."""
    from app.models.book import Book
    
    books = [
        Book(
            title=f"Book {i}",
            description=f"Description {i}",
            product_type="Book",
            price_excl_tax=10.00 + i,
            price_incl_tax=12.00 + i,
            tax=2.00,
            availability=5 + i,
            number_of_reviews=i,
            upc=f"test-upc-{i:03d}",
            rating=(i % 5) + 1,
            image_url=f"http://example.com/image{i}.jpg",
            category_id=sample_category.id,
        )
        for i in range(1, 6)
    ]
    
    test_db.add_all(books)
    test_db.commit()
    for book in books:
        test_db.refresh(book)
    
    return books

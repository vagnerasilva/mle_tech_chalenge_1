"""
tests/test_models.py — Testes unitários para modelos SQLAlchemy (Book, Category).
"""

import pytest
from app.models.book import Book, BookSchema
from app.models.category import Category, CategorySchema


class TestCategoryModel:
    """Testes para modelo Category."""
    
    def test_create_category(self, test_db):
        """Testa criação de categoria."""
        category = Category(name="Science Fiction")
        test_db.add(category)
        test_db.commit()
        
        assert category.id is not None
        assert category.name == "Science Fiction"
    
    def test_category_str(self, test_db):
        """Testa representação string de categoria."""
        category = Category(name="Mystery")
        test_db.add(category)
        test_db.commit()
        
        assert str(category) == "Mystery"
    
    def test_category_unique_name(self, test_db):
        """Testa constraint de nome único em categoria."""
        cat1 = Category(name="Fiction")
        cat2 = Category(name="Fiction")
        
        test_db.add(cat1)
        test_db.commit()
        
        test_db.add(cat2)
        with pytest.raises(Exception):  # IntegrityError
            test_db.commit()


class TestBookModel:
    """Testes para modelo Book."""
    
    def test_create_book(self, sample_book):
        """Testa criação de livro."""
        assert sample_book.id is not None
        assert sample_book.title == "Test Book"
        assert sample_book.price_incl_tax == 12.50
    
    def test_book_rating_constraint(self, test_db, sample_category):
        """Testa constraint de rating (0-5)."""
        book = Book(
            title="Invalid Rating Book",
            description="Test",
            product_type="Book",
            price_excl_tax=10.0,
            price_incl_tax=12.0,
            tax=2.0,
            availability=5,
            number_of_reviews=0,
            upc="invalid-rating",
            rating=10,  # Fora do intervalo
            image_url="http://example.com/image.jpg",
            category_id=sample_category.id,
        )
        test_db.add(book)
        with pytest.raises(Exception):  # CheckConstraintViolated
            test_db.commit()
    
    def test_book_upc_unique(self, test_db, sample_category):
        """Testa constraint de UPC único."""
        book1 = Book(
            title="Book 1",
            description="Test",
            product_type="Book",
            price_excl_tax=10.0,
            price_incl_tax=12.0,
            tax=2.0,
            availability=5,
            number_of_reviews=0,
            upc="same-upc",
            rating=3,
            image_url="http://example.com/image.jpg",
            category_id=sample_category.id,
        )
        book2 = Book(
            title="Book 2",
            description="Test",
            product_type="Book",
            price_excl_tax=10.0,
            price_incl_tax=12.0,
            tax=2.0,
            availability=5,
            number_of_reviews=0,
            upc="same-upc",  # Mesmo UPC
            rating=3,
            image_url="http://example.com/image.jpg",
            category_id=sample_category.id,
        )
        
        test_db.add(book1)
        test_db.commit()
        
        test_db.add(book2)
        with pytest.raises(Exception):  # IntegrityError
            test_db.commit()
    
    def test_book_relationship_with_category(self, sample_book, sample_category):
        """Testa relacionamento Book -> Category."""
        assert sample_book.category_id == sample_category.id
        assert sample_book.category.name == sample_category.name


class TestBookSchema:
    """Testes para schema Pydantic BookSchema."""
    
    def test_book_schema_from_orm(self, sample_book):
        """Testa conversão de Book ORM para BookSchema."""
        schema = BookSchema.model_validate(sample_book)
        
        assert schema.id == sample_book.id
        assert schema.title == sample_book.title
        assert schema.price_incl_tax == sample_book.price_incl_tax
    
    def test_book_schema_serialization(self, sample_book):
        """Testa serialização de BookSchema para dict."""
        schema = BookSchema.model_validate(sample_book)
        data = schema.model_dump()
        
        assert data["title"] == "Test Book"
        assert data["rating"] == 4
        assert "id" in data


class TestCategorySchema:
    """Testes para schema Pydantic CategorySchema."""
    
    def test_category_schema_from_orm(self, sample_category):
        """Testa conversão de Category ORM para CategorySchema."""
        schema = CategorySchema.model_validate(sample_category)
        
        assert schema.id == sample_category.id
        assert schema.name == sample_category.name

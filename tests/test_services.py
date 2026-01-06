"""
tests/test_services.py — Testes unitários para serviços de negócio.
"""

import pytest
import unittest
from unittest.mock import MagicMock, patch

from app.services.book import (
    get_books,
    get_books_between_prices,
    filter_books,
    get_best_book,
    get_book,
)
from app.services.category import get_categories
from app.services.stats import get_overview, get_category_overview
from fastapi import Request
from starlette.responses import StreamingResponse
from app.models.logs import ApiLog
from app.services.logs import write_log, get_logs
import uuid
import json


class TestBookService:
    """Testes para serviço de livros."""
    
    def test_get_books_empty_database(self, test_db):
        """Testa retorno vazio quando não há livros."""
        books = get_books(db=test_db)
        
        assert books == []
    
    def test_get_books_with_data(self, test_db, multiple_books):
        """Testa retorno de todos os livros."""
        books = get_books(db=test_db)
        
        assert len(books) == 5
        assert books[0].title == "Book 1"
    
    def test_get_book_by_id(self, test_db, sample_book):
        """Testa obtenção de livro por ID."""
        book = get_book(book_id=sample_book.id, db=test_db)
        
        assert book.id == sample_book.id
        assert book.title == "Test Book"
    
    def test_get_book_not_found(self, test_db):
        """Testa obtenção de livro não existente."""
        book = get_book(book_id=9999, db=test_db)
        
        assert book is None
    
    def test_get_best_book(self, test_db, sample_category):
        """Testa obtenção dos melhores livros (maior rating)."""
        from app.models.book import Book
        
        book1 = Book(
            title="Low Rated",
            description="Test",
            product_type="Book",
            price_excl_tax=10.0,
            price_incl_tax=12.0,
            tax=2.0,
            availability=5,
            number_of_reviews=10,
            upc="low-rated",
            rating=2,
            image_url="http://example.com/low.jpg",
            category_id=sample_category.id,
        )
        book2 = Book(
            title="High Rated",
            description="Test",
            product_type="Book",
            price_excl_tax=15.0,
            price_incl_tax=18.0,
            tax=3.0,
            availability=10,
            number_of_reviews=50,
            upc="high-rated",
            rating=5,
            image_url="http://example.com/high.jpg",
            category_id=sample_category.id,
        )
        
        test_db.add_all([book1, book2])
        test_db.commit()
        
        best = get_best_book(quant=1, db=test_db)
        
        assert best[0].title == "High Rated"
        assert best[0].rating == 5
    
    def test_get_books_between_prices(self, test_db, multiple_books):
        """Testa filtro de intervalo de preços."""
        # multiple_books cria 5 livros com preços: 10, 15, 20, 25, 30
        books = get_books_between_prices(db=test_db, min=15.0, max=25.0)
        
        assert len(books) == 3
        for book in books:
            assert 15.0 <= book.price_incl_tax <= 25.0
    
    def test_get_books_between_prices_no_results(self, test_db, multiple_books):
        """Testa intervalo de preços sem resultados."""
        books = get_books_between_prices(db=test_db, min=100.0, max=200.0)
        
        assert books == []
    
    def test_get_books_between_prices_invalid_range(self, test_db):
        """Testa intervalo inválido (min > max)."""
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException):
            get_books_between_prices(db=test_db, min=200.0, max=100.0)
    
    def test_filter_books_by_title(self, test_db, sample_book):
        """Testa filtro de livros por título."""
        books = filter_books(db=test_db, title="Test")
        
        assert len(books) >= 1
        assert any("Test" in book.title for book in books)
    
    def test_filter_books_no_results(self, test_db):
        """Testa filtro sem resultados."""
        books = filter_books(db=test_db, title="NonexistentBook")
        
        assert books == []


class TestCategoryService:
    """Testes para serviço de categorias."""
    
    def test_get_categories_empty(self, test_db):
        """Testa retorno vazio quando não há categorias."""
        categories = get_categories(db=test_db)
        
        assert categories == []
    
    def test_get_categories_returns_all(self, test_db):
        """Testa retorno de todas as categorias."""
        from app.models.category import Category
        
        cat1 = Category(name="Category 1")
        cat2 = Category(name="Category 2")
        cat3 = Category(name="Category 3")
        
        test_db.add_all([cat1, cat2, cat3])
        test_db.commit()
        
        categories = get_categories(db=test_db)
        
        assert len(categories) == 3
        names = [c.name for c in categories]
        assert "Category 1" in names
        assert "Category 2" in names


class TestStatsService:
    """Testes para serviço de estatísticas."""
    
    def test_get_overview_empty_db(self, test_db):
        """Testa estatísticas com DB vazio."""
        stats = get_overview(db=test_db)
        
        assert stats["total_books"] == 0
        assert stats["avg_rating"] is None or stats["avg_rating"] == 0
    
    def test_get_overview_with_data(self, test_db, multiple_books):
        """Testa estatísticas com dados."""
        stats = get_overview(db=test_db)
        
        assert stats["total_books"] == 5
        assert stats["avg_rating"] is not None
        assert 0 <= stats["avg_rating"] <= 5
    
    def test_get_category_overview_empty(self, test_db):
        """Testa estatísticas por categoria sem dados."""
        stats = get_category_overview(db=test_db)
        
        assert stats == []
    
    def test_get_category_overview_with_data(self, test_db, multiple_books, sample_category):
        """Testa estatísticas por categoria com dados."""
        stats = get_category_overview(db=test_db)
        
        assert len(stats) >= 1
        
        category_stat = next((s for s in stats if s["category"] == sample_category.name), None)
        assert category_stat is not None
        assert "total_books" in category_stat
        assert "avg_price" in category_stat


class TestLogs(unittest.TestCase):

    def setUp(self):
        # Mock do banco de dados
        self.db_mock = MagicMock()
        self.session_mock = MagicMock()
        self.db_mock.query.return_value.all.return_value = [ApiLog(id=1)]
        
        # Mock do Request
        self.req_mock = MagicMock(spec=Request)
        self.req_mock.headers = {"x-api-key": str(uuid.uuid4())}
        self.req_mock.client.host = "127.0.0.1"
        self.req_mock.url.path = "/test"
        self.req_mock.method = "POST"
        self.req_mock.query_params = {"param": "value"}
        self.req_mock.path_params = {"id": "123"}

        # Mock da Response
        self.res_mock = MagicMock(spec=StreamingResponse)
        self.res_mock.status_code = 200

    @patch("app.logs.get_db")
    def test_write_log_success(self, mock_get_db):
        mock_get_db.return_value = iter([self.db_mock])

        req_body = {"key": "value"}
        res_body = json.dumps({"result": "ok"})
        process_time = 0.123

        write_log(self.req_mock, self.res_mock, req_body, res_body, process_time)

        # Verifica se o log foi adicionado e commitado
        self.db_mock.add.assert_called_once()
        self.db_mock.commit.assert_called_once()
        self.db_mock.close.assert_called_once()

    def test_get_logs(self):
        logs = get_logs(self.db_mock)
        self.assertEqual(len(logs), 1)
        self.assertIsInstance(logs[0], ApiLog)

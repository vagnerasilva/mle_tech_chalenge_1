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


@pytest.fixture
def auth_client(test_db: Session, monkeypatch):
    """TestClient that bypasses AuthMiddleware by removing it from the app
    middleware stack and creating a fresh TestClient using the test DB.
    """
    from app.app import app as _app
    from app.dependencies import get_db as _get_db

    # Provide a fake GitHub client to avoid external HTTP calls during tests.
    class _FakeGitHubUser:
        def __init__(self, token=None):
            pass

        def get_authenticated(self):
            return type("R", (), {"parsed_data": {"login": "test-user"}})()


    class _FakeGitHub:
        def __init__(self, token=None):
            self.rest = type("R", (), {"users": _FakeGitHubUser()})

    monkeypatch.setattr("app.services.auth_middleware.GitHub", _FakeGitHub)

    # Backup and remove AuthMiddleware from the app.user_middleware list
    original_user_middleware = list(_app.user_middleware)
    _app.user_middleware = [m for m in _app.user_middleware if m.cls.__name__ != "AuthMiddleware"]

    # Rebuild the middleware stack so the change takes effect for new TestClient
    try:
        _app.build_middleware_stack()
    except Exception:
        # If rebuild isn't possible in the current state, continue; the TestClient
        # will build a fresh stack when instantiated in many cases.
        pass

    # Override the DB dependency to return the test DB
    def _override_get_db():
        return test_db

    _app.dependency_overrides[_get_db] = _override_get_db

    test_client = TestClient(_app)

    # Attempt to find the AuthMiddleware instance in the built middleware stack
    # and replace its dispatch with a lightweight bypass that injects a
    # test token into the session. This avoids depending on GitHub OAuth.
    try:
        import types

        async def _fake_dispatch(self, request, call_next):
            request.scope.setdefault("session", {})["access_token"] = "test-token"
            return await call_next(request)

        node = test_client.app.middleware_stack
        visited = 0
        while node and visited < 20:
            cls_name = getattr(node.__class__, "__name__", "")
            if cls_name == "AuthMiddleware":
                # bind the async function to the instance
                node.dispatch = types.MethodType(_fake_dispatch, node)
                break
            node = getattr(node, "app", None)
            visited += 1
    except Exception:
        # best-effort; if this fails we'll still yield the client and tests
        # will exercise existing behavior
        pass

    try:
        yield test_client
    finally:
        # restore original middleware list and clear overrides
        _app.user_middleware = original_user_middleware
        _app.dependency_overrides.pop(_get_db, None)


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

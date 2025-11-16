from app.models.base import Base, engine
from app.models.book import Book
from app.models.category import Category

# cria todas as tabelas definidas nos modelos
Base.metadata.create_all(bind=engine)

from app.models.base import Base, engine
from app.models.book import Book  # necessário para criar a tabela
from app.models.category import Category  # necessário para criar a tabela
# from app.models.logs import ApiLog


# cria todas as tabelas definidas nos modelos
Base.metadata.create_all(bind=engine)

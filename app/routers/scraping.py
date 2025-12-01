from fastapi import APIRouter, Depends
from app.services import scraping, category, book

from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.utils.constants import logger

router = APIRouter()


@router.get("/", response_model=str)
def popular_db_com_scraping(db: Session = Depends(get_db)):
    """Popula o banco de dados com as informações obtidas no site"""
    logger.info("Iniciando processo de scraping para popular o banco de dados")
    infos = scraping.scrape_books()
    logger.info("Obtendo informações de livros e categorias")
    categorias = scraping.get_categories()
    logger.info("Inserindo categorias e livros no banco de dados")
    category.post_categories(categorias, db)
    book.post_books(infos, db)
    return "Sucesso"

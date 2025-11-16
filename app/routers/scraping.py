from fastapi import APIRouter
from app.services import scraping, category, book

from fastapi import Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
router = APIRouter()


@router.get("/", response_model=str)
def popular_db_com_scraping(db: Session = Depends(get_db)):
    infos = scraping.scrape_books()
    categorias = scraping.get_categories()
    category.post_categories(categorias, db)
    book.post_books(infos, db)
    return "Sucesso"

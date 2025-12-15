from fastapi import APIRouter
from app.services import category
from app.utils.constants import logger

from fastapi import Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.category import CategorySchema

router = APIRouter()


@router.get("/", response_model=list[CategorySchema])
def lista_categorias(db: Session = Depends(get_db)):
    """Lista todas as categorias de livros"""
    logger.info("Obtendo lista de categorias")
    return category.get_categories(db)

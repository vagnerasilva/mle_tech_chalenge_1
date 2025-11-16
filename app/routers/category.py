from fastapi import APIRouter
from app.services import category

from fastapi import Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.category import CategorySchema

router = APIRouter()


@router.get("/", response_model=list[CategorySchema])
def lista_categorias(db: Session = Depends(get_db)):
    return category.get_categories(db)

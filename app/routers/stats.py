from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services import stats
from app.models.book import BookSchema
from app.models.stats import BookOverviewSchema, CategoryOverviewSchema
from typing import Optional
router = APIRouter()


@router.get("/overview", response_model=BookOverviewSchema)
def gera_estatisticas_gerais(db: Session = Depends(get_db)):
    """Gera as estatisticas gerais sobre os libros cadastrados."""
    return stats.get_overview(db)


@router.get("/categories", response_model=list[CategoryOverviewSchema])
def gera_estatisticas_por_categorias(db: Session = Depends(get_db)):
    "Gera estatisticas sobre as categorias"
    return stats.get_category_overview(db)

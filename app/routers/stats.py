from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services import stats
from app.models.stats import BookOverviewSchema, CategoryOverviewSchema
from app.utils.constants import logger
router = APIRouter()


@router.get("/overview", response_model=BookOverviewSchema)
def gera_estatisticas_gerais(db: Session = Depends(get_db)):
    """Gera as estatisticas gerais sobre os libros cadastrados."""
    logger.info("Gerando estatísticas gerais sobre os livros cadastrados")
    return stats.get_overview(db)


@router.get("/categories", response_model=list[CategoryOverviewSchema])
def gera_estatisticas_por_categorias(db: Session = Depends(get_db)):
    "Gera estatisticas sobre as categorias"
    logger.info("Gerando estatísticas por categoria")
    return stats.get_category_overview(db)

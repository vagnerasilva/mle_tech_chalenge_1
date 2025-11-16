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


@router.get("/top-rated", response_model=list[BookSchema])
def obter_melhores_livros(
    quant: Optional[int] = Query(
        5,
        description="Quantidade de livros a serem listados"
    ),
    db: Session = Depends(get_db)
):
    """Retorna os n livros com melhor avaliação, por padrão, os 5 melhores"""
    return stats.get_best_book(quant, db)


@router.get("/price-range", response_model=list[BookSchema])
def obter_livros_na_faixa_de_preco(
    min: float = Query(description="Menor preço"),
    max: float = Query(description="Maior preço"),
    db: Session = Depends(get_db)
):
    """Obtem os livros que estão em uma determinada faixa de preço"""
    return stats.get_books_between_prices(db, min, max)

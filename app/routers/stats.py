# GET /api/v1/stats/overview: estatísticas gerais da coleção (total de livros, preço médio, distribuição de ratings).
# •
# GET /api/v1/stats/categories: estatísticas detalhadas por categoria (quantidade de livros, preços por categoria).
# •
# GET /api/v1/books/top-rated: lista os livros com melhor avaliação (rating mais alto).
# •
# GET /api/v1/books/price-range?min={min}&max={max}: filtra livros dentro de uma faixa de preço específica.

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
    return stats.get_overview(db)


@router.get("/categories", response_model=list[CategoryOverviewSchema])
def gera_estatisticas_por_categorias(db: Session = Depends(get_db)):
    return stats.get_category_overview(db)


@router.get("/top-rated", response_model=list[BookSchema])
def obter_melhores_livros(
    quant: Optional[int] = Query(5, description="Quantidade de livros a serem listados com mehores avaliações"),
    db: Session = Depends(get_db)
):
    return stats.get_best_book(quant, db)


@router.get("/price-range", response_model=list[BookSchema])
def obter_livros_na_faixa_de_preco(
    min: float = Query(description="Menor preço"),
    max: float = Query(description="Maior preço"),
    db: Session = Depends(get_db)
):
    return stats.get_books_between_prices(db, min, max)

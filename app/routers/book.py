from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from app.services import book
from app.models.book import BookSchema
from app.dependencies import get_db
from typing import Optional

router = APIRouter()


@router.get("/", response_model=list[BookSchema])
def lista_books(db: Session = Depends(get_db)):
    """Lista as informações de todos os livros cadastrados"""
    return book.get_books(db)


@router.get("/search", response_model=list[BookSchema])
def pesquisar_books(
    title: Optional[str] = Query(None, description="Título do livro"),
    category: Optional[str] = Query(None, description="Categoria do livro"),
    db: Session = Depends(get_db)
):
    """Realiza busca de livro com base no titulo e/ou categoria
    """
    return book.filter_books(db, title, category)


@router.get("/{book_id}", response_model=BookSchema)
def obter_book(
    book_id: int = Path(
        description="O identificador único do book a ser buscado",
        ge=1),
    db: Session = Depends(get_db)
):
    """Busca por um livro especifico com base em seu ID"""
    # VAMOS SEGUIR COM O ID LITERAL OU UPC?
    return book.get_book(book_id, db)

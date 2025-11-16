from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.services import book
from app.models.book import BookSchema
from app.dependencies import get_db
from typing import Optional

router = APIRouter()


@router.get("/", response_model=list[BookSchema])
def lista_books(db: Session = Depends(get_db)):
    return book.get_books(db)


@router.get("/search", response_model=list[BookSchema])
def pesquisar_books(
    title: Optional[str] = Query(None, description="Título do livro"),
    category: Optional[str] = Query(None, description="Categoria do livro"),
    db: Session = Depends(get_db)
):
    return book.filter_books(db, title, category)


@router.get("/{book_id}", response_model=BookSchema)
def obter_book(book_id: int, db: Session = Depends(get_db)):
    # VAMOS SEGUIR COM O ID LITERAL OU UPC?
    return book.get_book(book_id, db)

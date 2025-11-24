from typing import List
from sqlalchemy.orm import Session
from app.models.book import Book, BookSchema
from app.services import category
from typing import Optional
from fastapi import HTTPException


def post_books(books_infos: List[dict], db: Session) -> None:
    for book in books_infos:
        book['category_id'] = category.get_category_id_by_name(book['category'], db)
        del book['category']
        exists = db.query(Book).filter_by(upc=book['upc']).first()
        if exists:
            print(f"Livro com UPC {book['upc']} já existe, ignorando inserção.")
            continue
        db.add(Book(**book))
    db.commit()


def get_book(book_id: int, db: Session) -> BookSchema:
    book = db.query(Book).filter(Book.id == book_id).first()
    return book


def get_books(db: Session) -> list[BookSchema]:
    books = db.query(Book).all()
    return books


def filter_books(
    db: Session,
    title: Optional[str] = None,
    category: Optional[str] = None,
) -> list[BookSchema]:
    query = db.query(Book)

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if category:
        query = query.join(Book.category).filter(Book.category.has(name=category))

    return query.all()


def get_best_book(quant, db) -> List[BookSchema]:
    books = db.query(Book).order_by(Book.rating.desc()).all()
    return books[:quant]


def get_books_between_prices(
    db: Session,
    min: float,
    max: float
):
    if min > max:
        raise HTTPException(
            status_code=400,
            detail="O valor mínimo não pode ser maior que o máximo"
            )

    return (
        db.query(Book)
        .filter(Book.price_incl_tax >= min, Book.price_incl_tax <= max)
        .all()
    )

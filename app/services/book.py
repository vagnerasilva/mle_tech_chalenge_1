from typing import List
from sqlalchemy.orm import Session
from app.models.book import Book
from app.services import category


def post_books(books_infos: List[dict], db: Session) -> None:
    for book in books_infos:
        book['category_id'] = category.get_category_id_by_name(book['category'], db)
        del book['category']
        db.add(Book(**book))
    db.commit()

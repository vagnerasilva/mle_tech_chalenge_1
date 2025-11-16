from app.models.category import Category
from fastapi import Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db


def post_categories(categories: list, db: Session):
    for category in categories:
        c = Category(**category)
        db.add(c)
    db.commit()


def get_category_id_by_name(name: str, db: Session) -> int:
    categoria = db.query(Category).filter(Category.name == name).first()
    return categoria.id

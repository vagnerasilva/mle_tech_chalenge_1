from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.stats import BookOverviewSchema, CategoryOverviewSchema
from app.models.category import Category
from sqlalchemy import func


def get_overview(db: Session) -> BookOverviewSchema:
    total_books = db.query(func.count(Book.id)).scalar()
    avg_price = db.query(func.avg(Book.price_incl_tax)).scalar()
    avg_rating = db.query(func.avg(Book.rating)).scalar()
    rating_dist = (
        db.query(Book.rating, func.count(Book.id))
        .group_by(Book.rating)
        .all()
    )

    return {
        "total_books": total_books,
        "avg_price": avg_price,
        "avg_rating": avg_rating,
        "distribution_rating": {rating: count for rating, count in rating_dist}
    }


def get_category_overview(db: Session) -> list[CategoryOverviewSchema]:
    results = (
        db.query(
            Category.name.label("category"),
            func.count(Book.id).label("total_books"),
            func.avg(Book.price_incl_tax).label("avg_price")
        )
        .join(Category, Book.category_id == Category.id)
        .group_by(Category.name)
        .all()
    )

    return [
        {
            "category": category_name,
            "total_books": total,
            "avg_price": round(preco_medio, 2) if preco_medio else None
        }
        for category_name, total, preco_medio in results
    ]

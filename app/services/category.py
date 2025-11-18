from app.models.category import Category, CategorySchema
from sqlalchemy.orm import Session


def post_categories(categories: list, db: Session):
    for category in categories:
        c = Category(**category)
        exists = db.query(Category).filter_by(name=category['name']).first()
        if exists:
            print(f"Categoria {category['name']} já existe, ignorando inserção.")
            continue
        db.add(c)
    db.commit()


def get_category_id_by_name(name: str, db: Session) -> int:
    category = db.query(Category).filter(Category.name == name).first()
    return category.id


def get_categories(db: Session) -> list[CategorySchema]:
    categories = db.query(Category).all()
    return categories

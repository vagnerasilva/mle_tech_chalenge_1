from book_scraping_model import db
from .category import Category

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    product_type = db.Column(db.Text, nullable=False)

    price_ex_tax = db.Column(db.Float, nullable=False)
    price_inc_tax = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)

    availability = db.Column(
        db.Integer,
        db.CheckConstraint("availability IN (0, 1)"),
        nullable=False
    )

    num_reviews = db.Column(
        db.Integer,
        default=0
    )

    upc = db.Column(db.Text, unique=True, nullable=False)

    rate = db.Column(
        db.Integer,
        db.CheckConstraint("rate BETWEEN 0 AND 5")
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    category = db.relationship("Category", backref="books")

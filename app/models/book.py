from sqlalchemy import (
    Column,
    Integer,
    Text,
    Float,
    ForeignKey,
    CheckConstraint
)
from sqlalchemy.orm import relationship
from app.models.base import Base
from pydantic import BaseModel


class BookSchema(BaseModel):
    id: int
    title: str
    description: str
    product_type: str
    price_excl_tax: float
    price_incl_tax: float
    tax: float
    availability: int
    number_of_reviews: int
    upc: str
    rating: int
    category_id: int
    image_url: str

    class Config:
        from_attributes = True   # permite converter de objetos SQLAlchemy


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    product_type = Column(Text, nullable=False)

    price_excl_tax = Column(Float, nullable=False)
    price_incl_tax = Column(Float, nullable=False)
    tax = Column(Float, nullable=False)

    availability = Column(
        Integer,
        nullable=False
    )

    number_of_reviews = Column(Integer, default=0)

    upc = Column(Text, unique=True, nullable=False)

    rating = Column(Integer, CheckConstraint("rating BETWEEN 0 AND 5"))

    image_url = Column(Text, nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", backref="books")

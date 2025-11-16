from sqlalchemy import Column, Integer, Text
from app.models.base import Base
from pydantic import BaseModel


class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True, nullable=False)

    def __str__(self):
        return self.name

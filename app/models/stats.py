from pydantic import BaseModel


class BookOverviewSchema(BaseModel):
    total_books: float
    avg_price: float
    avg_rating: float
    distribution_rating: dict

    class Config:
        from_attributes = True


class CategoryOverviewSchema(BaseModel):
    category: str
    total_books: int
    avg_price: float

    class Config:
        from_attributes = True

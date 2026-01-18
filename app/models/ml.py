from pydantic import BaseModel


class PredictionRequest(BaseModel):
    price: float
    rating: int
    category: str
    availability: int | None = None


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float

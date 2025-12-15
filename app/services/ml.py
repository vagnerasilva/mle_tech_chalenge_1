from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.ml import PredictionRequest, PredictionResponse


def get_features(db: Session):
    """
    Retorna apenas features úteis para ML.
    """
    books = db.query(Book).all()

    features = []
    for b in books:
        features.append({
            "id": b.id,
            "price": float(b.price),
            "rating": b.rating,
            "availability": 1 if b.availability else 0,
            "category": b.category.name
        })

    return features


def get_training_data(db: Session):
    """
    Retorna features + target fictício (ex: livro caro = 1, barato = 0).
    """
    books = db.query(Book).all()

    dataset = []

    for b in books:
        dataset.append({
            "id": b.id,
            "title": b.title,
            "price": float(b.price),
            "rating": b.rating,
            "availability": 1 if b.availability else 0,
            "category": b.category.name,
            # Target mockado — você define como quiser
            "label_is_expensive": 1 if b.price > 50 else 0
        })

    return {
        "columns": [
            "id", "title", "price", "rating",
            "availability", "category", "label_is_expensive"
        ],
        "data": dataset
    }


def predict(payload: PredictionRequest) -> PredictionResponse:
    """
    Predição mockada — apenas para demonstrar funcionamento do endpoint.
    """
    score = (payload.rating * 0.4) + (payload.price * 0.05)

    # regra mockada
    prediction = "recommended" if score > 10 else "not_recommended"

    return PredictionResponse(
        prediction=prediction,
        confidence=min(score / 20, 1.0)
    )

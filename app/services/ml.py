from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.ml import PredictionRequest, PredictionResponse


def get_features(db: Session):
    """
    Retorna features prontas pra analise do cientista
    """
    books = (
        db.query(Book)
        .join(Book.category) 
        .all()
    )

    features = []
    for b in books:
        features.append({
            "book_id": b.id,
            "title": b.title,
            "price_incl_tax": float(b.price_incl_tax), 
            "tax": float(b.tax),
            "availability": int(b.availability),
            "rating": int(b.rating) if b.rating is not None else None,
            "number_of_reviews": int(b.number_of_reviews or 0),
            "category": b.category.name
        })

    return features


def get_training_data(db: Session):
    """
    Retorna uma amostra de dados para o treinamento do modelo
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
            "category": b.category.name
        })

    return {
        "columns": [
            "id", "title", "price", "rating",
            "availability", "category"
        ],
        "data": dataset
    }


def predict(payload: PredictionRequest) -> PredictionResponse:
    """
    Predição mockada — apenas para demonstrar funcionamento do endpoint
    """
    score = (payload.rating * 0.4) + (payload.price * 0.05)

    # regra mockada
    prediction = "recommended" if score > 10 else "not_recommended"

    return PredictionResponse(
        prediction=prediction,
        confidence=min(score / 20, 1.0)
    )

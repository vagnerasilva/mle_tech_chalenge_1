from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.ml import PredictionRequest, PredictionResponse

def _minmax(value: float, minValue: float, maxValue: float) -> float:
    if value is None:
        return None
    elif minValue is None or maxValue is None or maxValue == minValue:
        return 0.0
    return (value - minValue) / (maxValue - minValue)

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
            "availability": int(b.availability or 0),
            "rating": int(b.rating) if b.rating is not None else None,
            "number_of_reviews": int(b.number_of_reviews or 0),
            "category": (b.category.name if b.category else "Unknown"),
        })

    return features

def get_features_normalized(db: Session):
    """
    Retorna features normalizadas
    """
    books = (
        db.query(Book)
        .join(Book.category) 
        .all()
    )

    prices = [float(b.price_incl_tax) for b in books if b.price_incl_tax is not None]
    taxes = [float(b.tax) for b in books if b.tax is not None]
    avails = [int(b.availability) for b in books if b.availability is not None]
    reviews = [int(b.number_of_reviews or 0) for b in books]
    ratings = [int(b.rating) for b in books if b.rating is not None]

    price_min, price_max = (min(prices), max(prices)) if prices else (None, None)
    tax_min, tax_max = (min(taxes), max(taxes)) if taxes else (None, None)
    avail_min, avail_max = (min(avails), max(avails)) if avails else (None, None)
    reviews_min, reviews_max = (min(reviews), max(reviews)) if reviews else (None, None)
    rating_min, rating_max = (min(ratings), max(ratings)) if ratings else (None, None)

    features = []
    for b in books:
        price = float(b.price_incl_tax) if b.price_incl_tax is not None else None
        tax = float(b.tax) if b.tax is not None else None
        availability = int(b.availability or 0)
        number_of_reviews = int(b.number_of_reviews or 0)

        rating = int(b.rating) if b.rating is not None else None

        features.append({
            "book_id": b.id,
            "category": b.category.name if getattr(b, "category", None) else "Unknown",

            "price_incl_tax_norm": _minmax(price, price_min, price_max),
            "tax_norm": _minmax(tax, tax_min, tax_max),
            "availability_norm": _minmax(float(availability), float(avail_min) if avail_min is not None else None, float(avail_max) if avail_max is not None else None),
            "number_of_reviews_norm": _minmax(float(number_of_reviews), float(reviews_min), float(reviews_max)),

            "rating_norm": _minmax(float(rating), float(rating_min) if rating_min is not None else None, float(rating_max) if rating_max is not None else None) if rating is not None else None,
            "rating_is_missing": rating is None,
        })

    # (opcional) devolver os parâmetros usados pra normalizar (transparência!)
    return {
        "scaler": {
            "price_incl_tax": {"min": price_min, "max": price_max},
            "tax": {"min": tax_min, "max": tax_max},
            "availability": {"min": avail_min, "max": avail_max},
            "number_of_reviews": {"min": reviews_min, "max": reviews_max},
            "rating": {"min": rating_min, "max": rating_max},
        },
        "data": features
    }

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

    prediction = "recommended" if score > 10 else "not_recommended"

    return PredictionResponse(
        prediction=prediction,
        confidence=min(score / 20, 1.0)
    )

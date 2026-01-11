from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.book import Book
from app.models.category import Category
from app.models.ml import MLFeature, TrainingData
from app.utils.constants import logger


def get_features(db: Session, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Obtém features normalizadas para consumo de modelos ML
    
    Args:
        db: Sessão do banco de dados
        limit: Limite de registros a retornar (None = todos)
    
    Returns:
        Dicionário contendo features, nomes de features e estatísticas
    """
    try:
        logger.info("Obtendo features para ML")
        
        query = db.query(
            Book.id,
            Book.title,
            Book.rating,
            Book.price_incl_tax,
            Book.availability,
            Book.number_of_reviews,
            Book.category_id,
            Category.name.label("category_name"),
            func.length(Book.description).label("description_length")
        ).join(Category, Book.category_id == Category.id)
        
        if limit:
            query = query.limit(limit)
        
        books = query.all()
        
        features = []
        for book in books:
            feature = MLFeature(
                book_id=book.id,
                title=book.title,
                rating=float(book.rating) / 5.0,
                price=book.price_incl_tax,
                availability=book.availability,
                number_of_reviews=book.number_of_reviews,
                category_id=book.category_id,
                category_name=book.category_name,
                description_length=book.description_length
            )
            features.append(feature)
        
        stats = _calculate_feature_statistics(features)
        
        feature_names = [
            "book_id",
            "rating",
            "price",
            "availability",
            "number_of_reviews",
            "category_id",
            "description_length"
        ]
        
        logger.info(f"Features obtidas com sucesso. Total: {len(features)}")
        
        return {
            "total_records": len(features),
            "features": features,
            "feature_names": feature_names,
            "statistics": stats
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter features: {e}")
        raise


def get_training_data(db: Session, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Obtém dataset completo para treinamento de modelos ML
    
    Args:
        db: Sessão do banco de dados
        limit: Limite de registros a retornar (None = todos)
    
    Returns:
        Dicionário contendo dados de treinamento e estatísticas
    """
    try:
        logger.info("Obtendo dataset de treinamento")
        
        query = db.query(Book).join(Category, Book.category_id == Category.id)
        
        if limit:
            query = query.limit(limit)
        
        books = query.all()
        
        training_data = []
        for book in books:
            data = TrainingData(
                book_id=book.id,
                title=book.title,
                description=book.description,
                product_type=book.product_type,
                price_excl_tax=book.price_excl_tax,
                price_incl_tax=book.price_incl_tax,
                tax=book.tax,
                availability=book.availability,
                number_of_reviews=book.number_of_reviews,
                upc=book.upc,
                rating=book.rating,
                category_id=book.category_id,
                category_name=book.category.name,
                image_url=book.image_url
            )
            training_data.append(data)
        
        categories_count = db.query(func.count(func.distinct(Category.id))).scalar()
        
        stats = _calculate_training_statistics(training_data)
        
        logger.info(f"Dataset de treinamento obtido. Total: {len(training_data)}")
        
        return {
            "total_records": len(training_data),
            "total_categories": categories_count,
            "data": training_data,
            "statistics": stats
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter dataset de treinamento: {e}")
        raise


def _calculate_feature_statistics(features: List[MLFeature]) -> Dict[str, Any]:
    """Calcula estatísticas das features"""
    if not features:
        return {}
    
    ratings = [f.rating for f in features]
    prices = [f.price for f in features]
    reviews = [f.number_of_reviews for f in features]
    availability = [f.availability for f in features]
    
    def _safe_avg(values):
        return sum(values) / len(values) if values else 0
    
    return {
        "rating_avg": _safe_avg(ratings),
        "rating_min": min(ratings) if ratings else 0,
        "rating_max": max(ratings) if ratings else 0,
        "price_avg": _safe_avg(prices),
        "price_min": min(prices) if prices else 0,
        "price_max": max(prices) if prices else 0,
        "reviews_avg": _safe_avg(reviews),
        "availability_avg": _safe_avg(availability),
    }


def _calculate_training_statistics(data: List[TrainingData]) -> Dict[str, Any]:
    """Calcula estatísticas do dataset de treinamento"""
    if not data:
        return {}
    
    ratings = [d.rating for d in data]
    prices = [d.price_incl_tax for d in data]
    reviews = [d.number_of_reviews for d in data]
    
    def _safe_avg(values):
        return sum(values) / len(values) if values else 0

    categories = set(d.category_id for d in data)
    
    return {
        "rating_distribution": {
            "avg": _safe_avg(ratings),
            "min": min(ratings) if ratings else 0,
            "max": max(ratings) if ratings else 0,
        },
        "price_distribution": {
            "avg": _safe_avg(prices),
            "min": min(prices) if prices else 0,
            "max": max(prices) if prices else 0,
        },
        "reviews_avg": _safe_avg(reviews),
        "unique_categories": len(categories),
        "unique_product_types": len(set(d.product_type for d in data))
    }

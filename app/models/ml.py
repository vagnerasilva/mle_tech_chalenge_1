from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class MLFeature(BaseModel):
    """Modelo para representar features normalizadas para ML"""
    book_id: int
    title: str
    rating: float = Field(..., description="Rating normalizado entre 0-5")
    price: float = Field(..., description="Preço inclusivo de imposto")
    availability: int = Field(..., description="Quantidade disponível")
    number_of_reviews: int
    category_id: int
    category_name: str
    description_length: int = Field(..., description="Tamanho da descrição")

    class Config:
        from_attributes = True


class TrainingData(BaseModel):
    """Modelo para dados de treinamento completos"""
    book_id: int
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
    category_name: str
    image_url: str

    class Config:
        from_attributes = True


class PredictionInput(BaseModel):
    """Modelo para entrada de predições"""
    features: Dict[str, Any] = Field(..., description="Features do livro para predição")


class PredictionOutput(BaseModel):
    """Modelo para saída de predições"""
    prediction: Any = Field(..., description="Resultado da predição")
    confidence: Optional[float] = Field(
        None,
        description="Score de confiança da predição (0-1)"
    )
    message: str


class MLDatasetResponse(BaseModel):
    """Modelo para resposta do dataset de treinamento"""
    total_records: int
    total_categories: int
    data: List[TrainingData]
    statistics: Dict[str, Any] = Field(..., description="Estatísticas dos dados")


class MLFeaturesResponse(BaseModel):
    """Modelo para resposta das features"""
    total_records: int
    features: List[MLFeature]
    feature_names: List[str]
    statistics: Dict[str, Any]

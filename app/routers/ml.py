from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.dependencies import get_db
from app.services import ml
from app.models.ml import (
    MLFeaturesResponse,
    MLDatasetResponse,
    PredictionInput,
    PredictionOutput
)
from app.utils.constants import logger

router = APIRouter()


@router.get(
    "/features",
    response_model=MLFeaturesResponse,
    summary="Obter features para ML",
    description="Retorna dados formatados como features para consumo de modelos ML"
)
def get_ml_features(
    limit: Optional[int] = Query(
        None,
        description="Limite de registros a retornar (None = todos)"
    ),
    db: Session = Depends(get_db)
):
    """
    Retorna features normalizadas para treinamento e predição de modelos ML.
    
    As features incluem:
    - book_id: Identificador único do livro
    - title: Título do livro
    - rating: Avaliação normalizada (0-1)
    - price: Preço inclusivo de imposto
    - availability: Quantidade em estoque
    - number_of_reviews: Número de avaliações
    - category_id: ID da categoria
    - category_name: Nome da categoria
    - description_length: Tamanho da descrição
    
    Também retorna estatísticas descritivas das features.
    """
    try:
        logger.info(f"Requisição de features com limite={limit}")
        result = ml.get_features(db, limit)
        
        return MLFeaturesResponse(
            total_records=result["total_records"],
            features=result["features"],
            feature_names=result["feature_names"],
            statistics=result["statistics"]
        )
    except Exception as e:
        logger.error(f"Erro ao obter features: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar features: {str(e)}"
        )


@router.get(
    "/training-data",
    response_model=MLDatasetResponse,
    summary="Obter dataset de treinamento",
    description="Retorna dataset completo para treinamento de modelos ML"
)
def get_training_dataset(
    limit: Optional[int] = Query(
        None,
        description="Limite de registros a retornar (None = todos)"
    ),
    db: Session = Depends(get_db)
):
    """
    Retorna dataset completo com todos os dados dos livros para treinamento.
    
    Inclui informações detalhadas de cada livro:
    - Título e descrição
    - Preços (com e sem imposto)
    - Avaliações e número de reviews
    - Disponibilidade
    - Categoria
    - Tipo de produto
    - UPC e URL da imagem
    
    Também inclui estatísticas gerais do dataset como distribuição de ratings,
    preços, número de categorias e tipos de produtos únicos.
    """
    try:
        logger.info(f"Requisição de dataset de treinamento com limite={limit}")
        result = ml.get_training_data(db, limit)
        
        return MLDatasetResponse(
            total_records=result["total_records"],
            total_categories=result["total_categories"],
            data=result["data"],
            statistics=result["statistics"]
        )
    except Exception as e:
        logger.error(f"Erro ao obter dataset de treinamento: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar dataset: {str(e)}"
        )


@router.post(
    "/predictions",
    response_model=PredictionOutput,
    summary="Receber predições do modelo ML",
    description="Endpoint para receber e processar predições de modelos ML"
)
def receive_predictions(
    prediction: PredictionInput,
    db: Session = Depends(get_db)
):
    """
    Recebe predições provenientes de modelos ML e as processa.
 
    Exemplo de entrada:
    ```json
    {
        "features": {
            "rating": 4.5,
            "price": 29.99,
            "number_of_reviews": 150,
            "category_id": 1
        }
    }
    ```
    """
    try:
        logger.info(
            f"Predição recebida, "
            f"features: {prediction.features}"
        )

        response_model = {'prediction_rating': "4"}
        
        response = PredictionOutput(
            prediction=response_model,
            confidence="0.47",
            message="Predição recebida e processada com sucesso - rota mockada para simular uso da rota"
        )
        
        logger.info(f"Predição processada: {response.message}")
        return response
        
    except ValueError as e:
        logger.error(f"Erro de validação na predição: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Dados de entrada inválidos: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Erro ao processar predição: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar predição: {str(e)}"
        )

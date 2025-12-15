from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services import ml
from app.models.ml import PredictionRequest, PredictionResponse

router = APIRouter()


@router.get("/features")
def get_features(db: Session = Depends(get_db)):
    """
    Retorna um dataset contendo apenas as features usadas para modelos de ML.
    """
    return ml.get_features(db)


@router.get("/training-data")
def get_training_data(db: Session = Depends(get_db)):
    """
    Retorna o dataset completo para treinamento.
    """
    return ml.get_training_data(db)


@router.post("/predictions", response_model=PredictionResponse)
def get_prediction(payload: PredictionRequest):
    """
    Recebe features e retorna uma predição mockada.
    """
    return ml.predict(payload)

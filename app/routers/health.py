from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.category import Category
from app.utils.constants import logger

router = APIRouter()


@router.get("/", response_model=dict)
def health_check(db: Session = Depends(get_db)):
    """Verifica status da API e conectividade com os dados."""
    try:
        logger.info("Verificando status do banco de dados")
        db.query(Category)
        db_status = "ok"
    except Exception:
        logger.error("Falha ao conectar ao banco de dados")
        db_status = "error"
    logger.info("Retornando status da API")
    return {
        "api_status": "ok",
        "database_status": db_status
    }

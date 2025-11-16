from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.category import Category

router = APIRouter()


@router.get("/", response_model=dict)
def health_check(db: Session = Depends(get_db)):
    """Verifica status da API e conectividade com os dados."""
    try:
        db.query(Category)
        db_status = "ok"
    except Exception:
        db_status = "error"

    return {
        "api_status": "ok",
        "database_status": db_status
    }

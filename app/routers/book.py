from fastapi import APIRouter, HTTPException
from app.services import book
from app.models.model import User

router = APIRouter()

@router.get("/", response_model=list[User])
def listar_books():
    return book.get_users()

@router.get("/{id}", response_model=User)
def obter_book(user_id: int):
    user = book.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

from typing import List
from app.models.model import User

# Simulação de banco de dados em memória
fake_users_db = [
    User(id=1, name="Ana", email="ana@example.com"),
    User(id=2, name="Bruno", email="bruno@example.com"),
]

def get_users() -> List[User]:
    return fake_users_db

def get_user_by_id(user_id: int) -> User | None:
    return next((user for user in fake_users_db if user.id == user_id), None)

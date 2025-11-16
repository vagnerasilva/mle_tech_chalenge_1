from app.models.base import SessionLocal


def get_db():
    print("chamou")
    db = SessionLocal()
    print("obteve a session")
    try:
        yield db
    finally:
        db.close()

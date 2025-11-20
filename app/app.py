from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.routers import (
    book,
    scraping,
    category,
    health,
    stats,
    login,
    logout,
    callback,
    home,
    nolog
)
from app.utils.constants import API_PREFIX
from starlette.middleware.sessions import SessionMiddleware
from app.settings import settings
from app.services.auth_middleware import AuthMiddleware

app = FastAPI(title="Books to scrap")

app.add_middleware(AuthMiddleware)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except SQLAlchemyError as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Erro no banco de dados.", "detail": f"{e}"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Erro interno inesperado.", "detail": f"{e}"}
        )

app.include_router(
    nolog.router,
    tags=["no_logged"]
)
app.include_router(
    home.router,
    prefix=f"{API_PREFIX}/home",
    tags=["home"]
)
app.include_router(
    login.router,
    prefix=f"/login",
    tags=["login"]
)
app.include_router(
    callback.router,
    prefix=f"/callback",
    tags=["callback"]
)
app.include_router(
        book.router,
        prefix=f"{API_PREFIX}/books",
        tags=["books"]
    )
app.include_router(
        scraping.router,
        prefix=f"{API_PREFIX}/scraping",
        tags=["scraping"]
    )
app.include_router(
        category.router,
        prefix=f"{API_PREFIX}/categories",
        tags=["categories"]
    )
app.include_router(
        health.router,
        prefix=f"{API_PREFIX}/health",
        tags=["health"]
    )
app.include_router(
        stats.router,
        prefix=f"{API_PREFIX}/stats",
        tags=["stats"]
    )
app.include_router(
        logout.router,
        prefix=f"{API_PREFIX}/logout",
        tags=["logout"]
    )

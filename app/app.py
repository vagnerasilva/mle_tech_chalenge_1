from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.routers import book, scraping, category, health, stats
from app.utils.constants import API_PREFIX

app = FastAPI(title="Books to scrap")


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

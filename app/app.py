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
    nolog,
    log
)
from app.utils.constants import API_PREFIX, logger
from starlette.middleware.sessions import SessionMiddleware
from app.settings import settings
from app.services.auth_middleware import AuthMiddleware
import time
from starlette.background import BackgroundTask
from starlette.concurrency import iterate_in_threadpool
from app.services.log import write_log

app = FastAPI(
    title="Books to scrap",
    description="Documentação da API",
    version="1.0.0",
    servers=[
        {"url": "https://mle-tech-chalenge-1.vercel.app/", "description": "Produção"},
        {"url": "http://localhost:8000/", "description": "Desenvolvimento"},
    ],
)
## Importante pra poder funcionar na porta principal do Vercel 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

app.add_middleware(AuthMiddleware)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        req_body = await request.json()
    except Exception:
        req_body = None

    try:
        logger.info(f"Recebida requisição: {request.method} {request.url.path}")
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        res_body = [section async for section in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(res_body))

        if res_body:
            try:
                res_body = res_body[0].decode()
            except Exception:
                res_body = None
        else:
            res_body = None

        # Add the background task to the response object to queue the job
        response.background = BackgroundTask(write_log, request, response, req_body, res_body, process_time)
        return response
    except SQLAlchemyError as e:
        logger.error(f"Erro no banco de dados: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": "Erro no banco de dados.", "detail": f"{e}"}
        )
    except Exception as e:
        logger.error(f"Erro interno inesperado: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": "Erro interno inesperado.", "detail": f"{e}"}
        )

app.include_router(
    nolog.router,
    tags=["no_logged"]
)
app.include_router(
    log.router,
    tags=["api_logs"]
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

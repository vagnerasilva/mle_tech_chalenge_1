from fastapi import FastAPI
from app.routers import book, scraping, category, health
from app.utils.constants import API_PREFIX

app = FastAPI(title="Books to scrap")

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

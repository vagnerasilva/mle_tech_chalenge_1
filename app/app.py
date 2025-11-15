from fastapi import FastAPI
from app.routers import book, scraping
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

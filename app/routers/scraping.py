from fastapi import APIRouter, HTTPException
from app.services import scraping

router = APIRouter()

@router.get("/")
def realizar_scraping():
    return scraping.scrape_books(1)

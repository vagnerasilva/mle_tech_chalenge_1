from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get('/')
async def logout(request: Request):
    """Rota para sair da api."""
    session = request.session
    session.clear()
    return RedirectResponse(url="/")

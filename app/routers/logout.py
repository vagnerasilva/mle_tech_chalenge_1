from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.utils.constants import logger

router = APIRouter()


@router.get('/')
async def logout(request: Request):
    """Rota para sair da api."""
    logger.info("Realizando logout do usuário")
    session = request.session
    session.clear()
    logger.info("Logout realizado com sucesso, redirecionando para /")
    return RedirectResponse(url="/")

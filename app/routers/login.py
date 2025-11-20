from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.settings import settings

router = APIRouter()


@router.get('/')
def login():
    """Rota que faz a autenticação e redireciona para o github"""
    # Monta a URL de autorização do GitHub
    redirect_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.CLIENT_ID}"
        f"&redirect_uri={settings.CallBack_URL}"
        f"&scope=user:email"
        f"&state={settings.SECRET_KEY}"
    )
    # Redireciona o usuário para o GitHub
    return RedirectResponse(url=redirect_url)

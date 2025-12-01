from app.settings import settings
from app.utils.constants import API_PREFIX, logger
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from githubkit import GitHub, OAuthAppAuthStrategy

router = APIRouter()


@router.get('/')
async def callback(req: Request):
    """Mostra a tela de autenticação.
    Mais informações: 
    https://medium.com/@bhuwan.pandey9867/github-authentication-with-python-fastapi-446a20e60d5a
    """
    logger.info("Iniciando callback de autenticação")
    session = req.session
    token = session.get("access_token", None)
    if token:
        logger.info("Usuário já autenticado, redirecionando para /home")
        return RedirectResponse(url=f"{API_PREFIX}/home")
    logger.info("Obtendo código de autenticação do GitHub")
    code = req.query_params.get('code')
    github = GitHub(OAuthAppAuthStrategy(settings.CLIENT_ID, settings.CLIENT_SECRET))
    auth = github.auth.as_web_user(code).exchange_token(github)
    access_token = auth.token
    session["access_token"] = access_token
    logger.info("Autenticação bem sucedida, redirecionando para /home")
    return RedirectResponse(url=f"{API_PREFIX}/home")

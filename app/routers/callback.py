from app.settings import settings
from app.utils.constants import API_PREFIX
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
    session = req.session
    token = session.get("access_token", None)
    if token:
        return RedirectResponse(url=f"{API_PREFIX}/home")
    code = req.query_params.get('code')
    github = GitHub(OAuthAppAuthStrategy(settings.CLIENT_ID, settings.CLIENT_SECRET))
    auth = github.auth.as_web_user(code).exchange_token(github)
    access_token = auth.token
    session["access_token"] = access_token
    return RedirectResponse(url=f"{API_PREFIX}/home")

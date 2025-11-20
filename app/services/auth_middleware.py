from fastapi import HTTPException
from githubkit import GitHub
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Essa classe é responsável por interceptar 
    as chamadas da api e validar se a autenticação foi realizada.
    """
    async def dispatch(self, request, call_next):
        rotas_publicas = ["/", "/login/", "/callback/",  "/callback",  "/api/v1/logout/"]

        if request.url.path in rotas_publicas:
            return await call_next(request)

        session = request.session
        access_token = session.get("access_token")

        if not access_token:
            raise HTTPException(
                status_code=401,
                detail="Não autenticado"
            )

        github = GitHub(access_token)

        try:
            resp = github.rest.users.get_authenticated()
            print(resp.parsed_data)
        except Exception:
            session.clear()
            return RedirectResponse("/login")

        return await call_next(request)

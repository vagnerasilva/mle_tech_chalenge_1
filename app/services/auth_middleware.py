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
        rotas_publicas = ["/", "/login/", "/login", "/callback/",  "/callback",  "/api/v1/logout/", "/docs", "/docs", "/openapi.json", "/favicon.ico"]

        if request.url.path in rotas_publicas:
            return await call_next(request)

        # Prefer token from session, but also support `Authorization: Bearer ...`
        # header to facilitate tests and alternative clients.
        session = getattr(request, "session", None)
        access_token = None
        if session is not None:
            access_token = session.get("access_token")

        if not access_token:
            auth_header = request.headers.get("authorization")
            if auth_header and auth_header.lower().startswith("bearer "):
                access_token = auth_header.split(None, 1)[1].strip()

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

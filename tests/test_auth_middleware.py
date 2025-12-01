"""
tests/test_auth_middleware.py — Testes para AuthMiddleware.

Cobre os seguintes cenários:
- rota pública: passa pelo call_next
- rota protegida sem token: levanta HTTPException 401
- rota protegida com token válido e GitHub OK: passa pelo call_next
- rota protegida com token inválido e GitHub lança exceção: redireciona para /login e limpa sessão

Os testes usam `starlette.requests.Request` criando um scope com `session` embutido
para simular a sessão (SessionMiddleware normalmente popula isso).
"""

import pytest
import types
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse
from app.services.auth_middleware import AuthMiddleware


@pytest.mark.asyncio
async def test_public_route_calls_next():
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "raw_path": b"/",
        "query_string": b"",
        "headers": [],
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
        "scheme": "http",
        "root_path": "",
        "http_version": "1.1",
        # session present but should not be inspected for public routes
        "session": {}
    }

    request = Request(scope)

    async def fake_call_next(req):
        return PlainTextResponse("ok", status_code=200)

    mw = AuthMiddleware(app=types.SimpleNamespace())
    resp = await mw.dispatch(request, fake_call_next)

    assert isinstance(resp, PlainTextResponse)
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_protected_route_no_token_raises():
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/protected",
        "raw_path": b"/protected",
        "query_string": b"",
        "headers": [],
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
        "scheme": "http",
        "root_path": "",
        "http_version": "1.1",
        "session": {}
    }

    request = Request(scope)

    async def fake_call_next(req):
        return PlainTextResponse("ok", status_code=200)

    mw = AuthMiddleware(app=types.SimpleNamespace())

    with pytest.raises(Exception) as excinfo:
        await mw.dispatch(request, fake_call_next)

    # should raise HTTPException with status_code 401
    assert getattr(excinfo.value, "status_code", None) == 401


@pytest.mark.asyncio
async def test_protected_route_with_token_and_github_ok(monkeypatch):
    # Prepare scope with session containing access_token
    session = {"access_token": "valid-token"}
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/protected",
        "raw_path": b"/protected",
        "query_string": b"",
        "headers": [],
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
        "scheme": "http",
        "root_path": "",
        "http_version": "1.1",
        "session": session
    }

    request = Request(scope)

    async def fake_call_next(req):
        return PlainTextResponse("ok", status_code=200)

    # Mock GitHub class used in middleware to simulate successful auth
    class FakeUsers:
        def get_authenticated(self):
            class Resp: 
                parsed_data = {"login": "user"}
            return Resp()

    class FakeRest:
        users = FakeUsers()

    class FakeGitHub:
        def __init__(self, token):
            self.access_token = token
            self.rest = FakeRest()

    monkeypatch.setattr("app.services.auth_middleware.GitHub", FakeGitHub)

    mw = AuthMiddleware(app=types.SimpleNamespace())
    resp = await mw.dispatch(request, fake_call_next)

    assert isinstance(resp, PlainTextResponse)
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_protected_route_with_token_and_github_fails(monkeypatch):
    # Prepare scope with session containing access_token
    session = {"access_token": "invalid-token"}
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/protected",
        "raw_path": b"/protected",
        "query_string": b"",
        "headers": [],
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
        "scheme": "http",
        "root_path": "",
        "http_version": "1.1",
        "session": session
    }

    request = Request(scope)

    async def fake_call_next(req):
        return PlainTextResponse("ok", status_code=200)

    # Mock GitHub class to raise on get_authenticated
    class FakeUsers:
        def get_authenticated(self):
            raise Exception("invalid token")

    class FakeRest:
        users = FakeUsers()

    class FakeGitHub:
        def __init__(self, token):
            self.access_token = token
            self.rest = FakeRest()

    monkeypatch.setattr("app.services.auth_middleware.GitHub", FakeGitHub)

    mw = AuthMiddleware(app=types.SimpleNamespace())
    resp = await mw.dispatch(request, fake_call_next)

    # Should be a RedirectResponse to /login and session cleared
    assert isinstance(resp, RedirectResponse)
    assert resp.status_code in (307, 302)
    # session should be cleared by middleware
    assert session == {}

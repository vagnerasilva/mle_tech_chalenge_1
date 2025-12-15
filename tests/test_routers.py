"""
tests/test_routers.py — Testes de integração para rotas/endpoints FastAPI.
"""

import pytest
from fastapi import status


class TestPublicRoutes:
    """Testes para rotas públicas (sem autenticação)."""
    
    def test_home_endpoint(self, client):
        """Testa endpoint home."""
        response = client.get("/")
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_307_TEMPORARY_REDIRECT]
    
    def test_login_redirect(self, client):
        """Testa endpoint de login (redireciona para GitHub)."""
        response = client.get("/login/", follow_redirects=False)
        
        # Login deve redirecionar para GitHub OAuth
        assert response.status_code in [status.HTTP_307_TEMPORARY_REDIRECT, status.HTTP_302_FOUND]
        assert "github.com" in response.headers.get("location", "").lower()


class TestHealthRouterWithoutAuth:
    """Testes para rota /health (nota: requer auth middleware bypass para testes)."""
    def test_health_endpoint_success(self, auth_client):
        """Testa endpoint de health check com sessão autenticada."""
        response = auth_client.get("/api/v1/health/", headers={"Authorization": "Bearer test-token"})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "api_status" in data


class TestBooksEndpointsWithoutAuth:
    """Testes para endpoints de livros (requerem auth por middleware)."""
    def test_get_books(self, auth_client, multiple_books):
        """Testa obtenção de livros com sessão autenticada."""
        response = auth_client.get("/api/v1/books/", headers={"Authorization": "Bearer test-token"})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 5


class TestCategoriesEndpointsWithoutAuth:
    """Testes para endpoints de categorias (requerem auth por middleware)."""
    def test_get_categories(self, auth_client, sample_category):
        """Testa obtenção de categorias com sessão autenticada."""
        response = auth_client.get("/api/v1/categories/", headers={"Authorization": "Bearer test-token"})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1


class TestStatsEndpointsWithoutAuth:
    """Testes para endpoints de estatísticas (requerem auth por middleware)."""
    def test_get_stats_overview(self, auth_client, multiple_books):
        """Testa estatísticas gerais com sessão autenticada."""
        response = auth_client.get("/api/v1/stats/overview", headers={"Authorization": "Bearer test-token"})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_books" in data

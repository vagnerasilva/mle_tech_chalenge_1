import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.app import app
from app.dependencies import get_db
from tests.conftest import TestingSessionLocal, create_test_data


client = TestClient(app)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


class TestMLEndpoints:
    """Testes para os endpoints de ML"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada teste"""
        db = TestingSessionLocal()
        create_test_data(db)
        db.close()
        yield
        # Cleanup
        db = TestingSessionLocal()
        db.query_all().delete()
        db.commit()
        db.close()

    def test_get_features(self):
        """Testa o endpoint GET /api/v1/ml/features"""
        response = client.get("/api/v1/ml/features")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "total_records" in data
        assert "features" in data
        assert "feature_names" in data
        assert "statistics" in data
        
        assert data["total_records"] > 0
        assert len(data["features"]) == data["total_records"]
        
        # Validar estrutura das features
        feature = data["features"][0]
        assert "book_id" in feature
        assert "title" in feature
        assert "rating" in feature
        assert "price" in feature
        assert "availability" in feature
        assert "number_of_reviews" in feature
        assert "category_id" in feature
        assert "category_name" in feature
        assert "description_length" in feature

    def test_get_features_with_limit(self):
        """Testa o endpoint GET /api/v1/ml/features com limit"""
        response = client.get("/api/v1/ml/features?limit=5")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_records"] <= 5

    def test_get_training_data(self):
        """Testa o endpoint GET /api/v1/ml/training-data"""
        response = client.get("/api/v1/ml/training-data")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "total_records" in data
        assert "total_categories" in data
        assert "data" in data
        assert "statistics" in data
        
        assert data["total_records"] > 0
        assert len(data["data"]) == data["total_records"]
        
        # Validar estrutura dos dados de treinamento
        training_record = data["data"][0]
        assert "book_id" in training_record
        assert "title" in training_record
        assert "description" in training_record
        assert "product_type" in training_record
        assert "price_excl_tax" in training_record
        assert "price_incl_tax" in training_record
        assert "rating" in training_record
        assert "category_id" in training_record
        assert "category_name" in training_record

    def test_get_training_data_with_limit(self):
        """Testa o endpoint GET /api/v1/ml/training-data com limit"""
        response = client.get("/api/v1/ml/training-data?limit=5")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_records"] <= 5

    def test_post_predictions(self):
        """Testa o endpoint POST /api/v1/ml/predictions"""
        prediction_data = {
            "features": {
                "rating": 4.5,
                "price": 29.99,
                "number_of_reviews": 150,
                "category_id": 1
            },
            "model_type": "recommendation"
        }
        
        response = client.post("/api/v1/ml/predictions", json=prediction_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "prediction" in data
        assert "model_type" in data
        assert "message" in data
        assert data["model_type"] == "recommendation"
        assert "sucesso" in data["message"].lower()

    def test_features_statistics(self):
        """Testa se as estatísticas são calculadas corretamente"""
        response = client.get("/api/v1/ml/features")
        
        assert response.status_code == 200
        data = response.json()
        stats = data["statistics"]
        
        # Validar que estatísticas foram calculadas
        assert "rating_avg" in stats
        assert "price_avg" in stats
        assert "reviews_avg" in stats
        assert "availability_avg" in stats

    def test_training_data_statistics(self):
        """Testa se as estatísticas do dataset são calculadas corretamente"""
        response = client.get("/api/v1/ml/training-data")
        
        assert response.status_code == 200
        data = response.json()
        stats = data["statistics"]
        
        # Validar que estatísticas foram calculadas
        assert "rating_distribution" in stats
        assert "price_distribution" in stats
        assert "reviews_avg" in stats
        assert "unique_categories" in stats
        assert "unique_product_types" in stats

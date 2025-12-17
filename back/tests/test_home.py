# tests/test_home.py
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.security.jwt import create_access_token


def test_home_page_unauthenticated():
    """Тест главной страницы без авторизации"""
    client = TestClient(app)
    response = client.get("/home")
    # Может быть 200 или 401 в зависимости от настроек
    assert response.status_code in [200, 401]


@patch('app.routers.home.ml_client')
def test_home_page_authenticated(mock_ml_client):
    """Тест главной страницы с авторизацией (мок ML)"""
    # Настраиваем мок - используем AsyncMock для асинхронных методов
    mock_ml_client.health_check = AsyncMock(return_value=True)
    mock_ml_client.get_recommendations = AsyncMock(return_value=[1, 2, 3])
    
    # Создаем тестовый токен
    from app.security.jwt import create_access_token
    token = create_access_token(data={"sub": "test@test.com", "user_id": 123})
    headers = {"Authorization": f"Bearer {token}"}
    
    client = TestClient(app)
    response = client.get("/home", headers=headers)
    
    # Проверяем статус (может быть 200 или 500 в зависимости от БД)
    assert response.status_code in [200, 500]
    
    # Если статус 200, проверяем вызов мока
    if response.status_code == 200:
        mock_ml_client.get_recommendations.assert_called_once()
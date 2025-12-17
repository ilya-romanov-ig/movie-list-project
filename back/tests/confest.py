# back/tests/conftest.py
import pytest
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

# Добавляем путь к app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Устанавливаем переменные окружения для тестов
os.environ["TESTING"] = "True"
os.environ["JWT_SECRET"] = "test_secret_key_for_testing_only"
os.environ["ML_SERVICE_URL"] = "http://ml-mock:8000"

# Импортируем app после установки переменных окружения
from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture(scope="session")
def test_client():
    """Фикстура для TestClient"""
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_db():
    """Фикстура для мока базы данных"""
    return AsyncMock()

@pytest.fixture
def auth_token():
    """Создание тестового токена"""
    from app.security.jwt import create_access_token
    return create_access_token({"sub": "1", "user_id": 1})

@pytest.fixture
def auth_headers(auth_token):
    """Заголовки с авторизацией"""
    return {"Authorization": f"Bearer {auth_token}"}

# Глобальные моки для всех тестов
@pytest.fixture(autouse=True)
def mock_external_deps():
    """Автоматически мокаем внешние зависимости"""
    # Мокаем ML клиент
    with patch('app.clients.ml_client.MLClient') as MockMLClient:
        mock_instance = AsyncMock()
        mock_instance.health_check.return_value = True
        mock_instance.get_recommendations.return_value = [1, 2, 3, 4, 5]
        MockMLClient.return_value = mock_instance
        yield

    # Мокаем базу данных
    with patch('app.db.get_db') as mock_get_db:
        mock_session = AsyncMock()
        mock_get_db.return_value = mock_session
        yield
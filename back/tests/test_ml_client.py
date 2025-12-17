# tests/test_ml_client.py
import pytest
import respx
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
from app.clients.ml_client import MLClient


@pytest.mark.asyncio
async def test_ml_client_health_check_success():
    """Тест health check ML сервиса (успех)"""
    with respx.mock:
        # Мокаем запрос
        respx.get("http://movie-recommender:8000/health").mock(
            return_value=httpx.Response(200, json={"status": "healthy"})
        )
        
        client = MLClient()
        # Важно: в тестах нужно мокать создание клиента
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_client.get.return_value = mock_response
        client._client = mock_client  # Подменяем клиент
        
        is_healthy = await client.health_check()
        assert is_healthy is True


@pytest.mark.asyncio
async def test_ml_client_get_recommendations():
    """Тест получения рекомендаций"""
    with respx.mock:
        mock_response = {
            "recommendations": [101, 102, 103],
            "user_id": 123,
            "count": 3
        }
        
        respx.get("http://movie-recommender:8000/recommend/123").mock(
            return_value=httpx.Response(200, json=mock_response)
        )
        
        client = MLClient()
        
        # Создаем мок для httpx клиента
        mock_httpx_client = AsyncMock()
        mock_http_response = AsyncMock()
        mock_http_response.status_code = 200
        mock_http_response.json.return_value = mock_response
        mock_httpx_client.get.return_value = mock_http_response
        
        # Подменяем клиент
        client._client = mock_httpx_client
        
        recommendations = await client.get_recommendations(123, count=3)
        assert recommendations == [101, 102, 103]


@pytest.mark.asyncio
async def test_ml_client_with_mock_simple():
    """Упрощенный тест с моком"""
    # Создаем экземпляр клиента
    client = MLClient()
    
    # Создаем мок для response
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"recommendations": [1, 2, 3]}
    
    # Создаем мок для httpx клиента
    mock_httpx_client = AsyncMock()
    mock_httpx_client.get.return_value = mock_response
    
    # Подменяем клиент в нашем MLClient
    client._client = mock_httpx_client
    
    # Вызываем метод
    result = await client.get_recommendations(123)
    
    # Проверяем результат
    assert result == [1, 2, 3]
    
    # Проверяем, что get был вызван с правильными параметрами
    mock_httpx_client.get.assert_called_once_with(
        "http://movie-recommender:8000/recommend/123",
        params={"count": 10}
    )
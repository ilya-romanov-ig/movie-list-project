# tests/test_auth.py
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.security.jwt import create_access_token


@pytest.fixture
def client():
    return TestClient(app)


def test_register_success():
    """Тест успешной регистрации"""
    client = TestClient(app)
    
    with patch('app.routers.auth.async_session') as mock_session:
        mock_session_instance = AsyncMock()
        mock_session.return_value.__aenter__.return_value = mock_session_instance
        
        # Настраиваем мок скаляра
        mock_session_instance.scalar.return_value = None
        
        response = client.post(
            "/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["msg"] == "OK"
        assert "id" in data


def test_register_user_exists():
    """Тест регистрации существующего пользователя"""
    client = TestClient(app)
    
    with patch('app.routers.auth.async_session') as mock_session:
        mock_session_instance = AsyncMock()
        mock_session.return_value.__aenter__.return_value = mock_session_instance
        
        # Возвращаем существующего пользователя
        mock_user = AsyncMock()
        mock_session_instance.scalar.return_value = mock_user
        
        response = client.post(
            "/auth/register",
            json={
                "username": "existinguser",
                "email": "existing@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 400
        assert "User already exists" in response.json()["detail"]


def test_register_missing_fields():
    """Тест регистрации с отсутствующими полями"""
    client = TestClient(app)
    
    # Тест без username
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 422  # Validation error


def test_login_success():
    """Тест успешного входа"""
    client = TestClient(app)
    
    with patch('app.routers.auth.async_session') as mock_session:
        mock_session_instance = AsyncMock()
        mock_session.return_value.__aenter__.return_value = mock_session_instance
        
        # Создаем мок пользователя
        mock_user = AsyncMock()
        mock_user.user_id = 1
        mock_user.email = "test@example.com"
        mock_user.password_hash = "$2b$12$..."  # Mock hashed password
        
        mock_session_instance.scalar.return_value = mock_user
        
        # Мокаем verify_password
        with patch('app.routers.auth.verify_password', return_value=True):
            response = client.post(
                "/auth/login",
                data={
                    "username": "test@example.com",
                    "password": "password123"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"


def test_login_invalid_credentials():
    """Тест входа с неверными учетными данными"""
    client = TestClient(app)
    
    with patch('app.routers.auth.async_session') as mock_session:
        mock_session_instance = AsyncMock()
        mock_session.return_value.__aenter__.return_value = mock_session_instance
        
        # Пользователь не найден
        mock_session_instance.scalar.return_value = None
        
        response = client.post(
            "/auth/login",
            data={
                "username": "wrong@example.com",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]


# def test_get_me_success():
#     """Тест получения информации о текущем пользователе"""
#     # Создаем тестовый токен
#     token = create_access_token({"sub": "1"})
    
#     client = TestClient(app)
    
#     # Мокаем get_current_user
#     with patch('app.routers.auth.get_current_user') as mock_get_user:
#         mock_user = AsyncMock()
#         mock_user.user_id = 1
#         mock_user.username = "testuser"
#         mock_user.email = "test@example.com"
#         mock_get_user.return_value = mock_user
        
#         response = client.get(
#             "/auth/me",
#             headers={"Authorization": f"Bearer {token}"}
#         )
        
#         assert response.status_code == 200
#         data = response.json()
#         assert data["id"] == 1
#         assert data["username"] == "testuser"
#         assert data["email"] == "test@example.com"


def test_get_me_no_token():
    """Тест получения информации без токена"""
    client = TestClient(app)
    response = client.get("/auth/me")
    
    assert response.status_code == 401


def test_get_me_invalid_token():
    """Тест получения информации с недействительным токеном"""
    client = TestClient(app)
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    assert response.status_code == 401
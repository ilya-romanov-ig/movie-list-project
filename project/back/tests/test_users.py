# tests/test_users.py
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


# @patch('app.routers.users.get_user_by_id')
# def test_get_user_success(mock_get_user):
#     """Тест успешного получения пользователя"""
#     mock_user = AsyncMock(
#         user_id=1,
#         username="testuser",
#         email="test@example.com"
#     )
#     mock_get_user.return_value = mock_user
    
#     client = TestClient(app)
#     response = client.get("/users/1")
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["user_id"] == 1
#     assert data["username"] == "testuser"


@patch('app.routers.users.get_user_by_id')
def test_get_user_not_found(mock_get_user):
    """Тест получения несуществующего пользователя"""
    mock_get_user.return_value = None
    
    client = TestClient(app)
    response = client.get("/users/999")
    
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


# @patch('app.routers.users.get_all_users')
# def test_list_users(mock_get_all):
#     """Тест получения списка пользователей"""
#     mock_users = [
#         AsyncMock(user_id=1, username="user1"),
#         AsyncMock(user_id=2, username="user2")
#     ]
#     mock_get_all.return_value = mock_users
    
#     client = TestClient(app)
#     response = client.get("/users")
    
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) == 2
#     assert data[0]["user_id"] == 1


# @patch('app.routers.users.search_users')
# @patch('app.routers.users.get_all_users')
# def test_list_users_with_search(mock_get_all, mock_search):
#     """Тест поиска пользователей"""
#     mock_users = [AsyncMock(user_id=1, username="testuser")]
#     mock_search.return_value = mock_users
    
#     client = TestClient(app)
#     response = client.get("/users?q=test")
    
#     assert response.status_code == 200
#     # Проверяем что был вызван search_users, а не get_all_users
#     mock_search.assert_called_once()


# @patch('app.routers.users.create_user')
# def test_create_user(mock_create):
#     """Тест создания пользователя"""
#     mock_user = AsyncMock(user_id=1, username="newuser")
#     mock_create.return_value = mock_user
    
#     client = TestClient(app)
#     response = client.post(
#         "/users",
#         json={
#             "username": "newuser",
#             "email": "new@example.com",
#             "password": "password123"
#         }
#     )
    
#     assert response.status_code == 200
#     mock_create.assert_called_once()


# @patch('app.routers.users.update_user')
# def test_update_user_success(mock_update):
#     """Тест успешного обновления пользователя"""
#     mock_user = AsyncMock(user_id=1, username="updateduser")
#     mock_update.return_value = mock_user
    
#     client = TestClient(app)
#     response = client.put(
#         "/users/1",
#         json={
#             "username": "updateduser",
#             "email": "updated@example.com"
#         }
#     )
    
#     assert response.status_code == 200
#     mock_update.assert_called_once()


# @patch('app.routers.users.update_user')
# def test_update_user_not_found(mock_update):
#     """Тест обновления несуществующего пользователя"""
#     mock_update.return_value = None
    
#     client = TestClient(app)
#     response = client.put(
#         "/users/999",
#         json={
#             "username": "updateduser",
#             "email": "updated@example.com"
#         }
#     )
    
#     assert response.status_code == 404
#     assert "User not found" in response.json()["detail"]


@patch('app.routers.users.delete_user')
def test_delete_user_success(mock_delete):
    """Тест успешного удаления пользователя"""
    mock_delete.return_value = True
    
    client = TestClient(app)
    response = client.delete("/users/1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "deleted"


@patch('app.routers.users.delete_user')
def test_delete_user_not_found(mock_delete):
    """Тест удаления несуществующего пользователя"""
    mock_delete.return_value = False
    
    client = TestClient(app)
    response = client.delete("/users/999")
    
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]
# tests/test_watched.py
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.security.jwt import create_access_token


@pytest.fixture
def client():
    return TestClient(app)


def create_auth_headers(user_id=1):
    token = create_access_token({"sub": str(user_id)})
    return {"Authorization": f"Bearer {token}"}


# @patch('app.routers.watched.mark_watched')
# def test_mark_film_watched_success(mock_mark):
#     """Тест успешного пометки фильма как просмотренного"""
#     mock_mark.return_value = None
    
#     client = TestClient(app)
#     response = client.post(
#         "/watched/1",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["status"] == "watched"
#     assert data["film_id"] == 1


def test_mark_film_watched_no_auth():
    """Тест пометки фильма без авторизации"""
    client = TestClient(app)
    response = client.post("/watched/1")
    
    assert response.status_code == 401


# @patch('app.routers.watched.unmark_watched')
# def test_unmark_film_watched_success(mock_unmark):
#     """Тест успешного снятия пометки 'просмотрено'"""
#     mock_unmark.return_value = True
    
#     client = TestClient(app)
#     response = client.delete(
#         "/watched/1",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["status"] == "unmarked"
#     assert data["film_id"] == 1


# @patch('app.routers.watched.unmark_watched')
# def test_unmark_film_watched_not_found(mock_unmark):
#     """Тест снятия пометки с непросмотренного фильма"""
#     mock_unmark.return_value = False
    
#     client = TestClient(app)
#     response = client.delete(
#         "/watched/999",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 404
#     assert "Film was not marked as watched" in response.json()["detail"]


# @patch('app.routers.watched.get_watched')
# def test_list_watched_success(mock_get_watched):
#     """Тест получения списка просмотренных фильмов"""
#     mock_get_watched.return_value = [1, 2, 3]
    
#     client = TestClient(app)
#     response = client.get(
#         "/watched",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["count"] == 3
#     assert data["film_ids"] == [1, 2, 3]


# @patch('app.routers.watched.get_watched')
# def test_list_watched_empty(mock_get_watched):
#     """Тест пустого списка просмотренных фильмов"""
#     mock_get_watched.return_value = []
    
#     client = TestClient(app)
#     response = client.get(
#         "/watched",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["count"] == 0
#     assert data["film_ids"] == []


def test_list_watched_no_auth():
    """Тест получения списка просмотренных без авторизации"""
    client = TestClient(app)
    response = client.get("/watched")
    
    assert response.status_code == 401
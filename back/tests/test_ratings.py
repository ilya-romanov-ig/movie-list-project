# tests/test_ratings.py
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


@patch('app.routers.ratings.get_ratings_for_film')
def test_list_film_ratings(mock_get_ratings):
    """Тест получения рейтингов фильма"""
    mock_ratings = [
        AsyncMock(user_id=1, rating=8),
        AsyncMock(user_id=2, rating=9)
    ]
    mock_get_ratings.return_value = mock_ratings
    
    client = TestClient(app)
    response = client.get("/ratings/1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["items"][0]["user_id"] == 1
    assert data["items"][0]["rating"] == 8


@patch('app.routers.ratings.get_avg_rating')
def test_avg_rating(mock_get_avg):
    """Тест получения среднего рейтинга"""
    mock_get_avg.return_value = 8.5
    
    client = TestClient(app)
    response = client.get("/ratings/1/avg")
    
    assert response.status_code == 200
    data = response.json()
    assert data["film_id"] == 1
    assert data["avg_rating"] == 8.5


# @patch('app.routers.ratings.set_rating')
# def test_rate_film_success(mock_set_rating):
#     """Тест успешной оценки фильма"""
#     mock_rating = AsyncMock(user_id=1, film_id=1, rating=9)
#     mock_set_rating.return_value = mock_rating
    
#     client = TestClient(app)
#     response = client.post(
#         "/ratings/1?rating=9",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["status"] == "ok"
#     assert data["film_id"] == 1
#     assert data["rating"] == 9


# def test_rate_film_invalid_rating_low():
#     """Тест оценки с рейтингом ниже допустимого"""
#     client = TestClient(app)
#     response = client.post(
#         "/ratings/1?rating=0",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 422  # Validation error


# def test_rate_film_invalid_rating_high():
#     """Тест оценки с рейтингом выше допустимого"""
#     client = TestClient(app)
#     response = client.post(
#         "/ratings/1?rating=11",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 422  # Validation error


def test_rate_film_no_auth():
    """Тест оценки фильма без авторизации"""
    client = TestClient(app)
    response = client.post("/ratings/1?rating=8")
    
    assert response.status_code == 401


# @patch('app.routers.ratings.delete_rating')
# def test_remove_rating_success(mock_delete_rating):
#     """Тест успешного удаления рейтинга"""
#     mock_delete_rating.return_value = True
    
#     client = TestClient(app)
#     response = client.delete(
#         "/ratings/1",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["status"] == "deleted"
#     assert data["film_id"] == 1


# @patch('app.routers.ratings.delete_rating')
# def test_remove_rating_not_found(mock_delete_rating):
#     """Тест удаления несуществующего рейтинга"""
#     mock_delete_rating.return_value = False
    
#     client = TestClient(app)
#     response = client.delete(
#         "/ratings/999",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 404
#     assert "Rating not found" in response.json()["detail"]


def test_remove_rating_no_auth():
    """Тест удаления рейтинга без авторизации"""
    client = TestClient(app)
    response = client.delete("/ratings/1")
    
    assert response.status_code == 401
# tests/test_favorites.py
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


# --------------------------
# Тесты для избранных фильмов
# --------------------------

# @patch('app.routers.favorites.add_favorite_film')
# def test_add_favorite_film_success(mock_add_favorite):
#     """Тест успешного добавления фильма в избранное"""
#     mock_add_favorite.return_value = None
    
#     client = TestClient(app)
#     response = client.post(
#         "/favorites/films/1",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["status"] == "added"
#     assert data["film_id"] == 1


def test_add_favorite_film_no_auth():
    """Тест добавления фильма в избранное без авторизации"""
    client = TestClient(app)
    response = client.post("/favorites/films/1")
    
    assert response.status_code == 401


# @patch('app.routers.favorites.remove_favorite_film')
# def test_remove_favorite_film_success(mock_remove_favorite):
#     """Тест успешного удаления фильма из избранного"""
#     mock_remove_favorite.return_value = True
    
#     client = TestClient(app)
#     response = client.delete(
#         "/favorites/films/1",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["status"] == "removed"
#     assert data["film_id"] == 1


# @patch('app.routers.favorites.remove_favorite_film')
# def test_remove_favorite_film_not_found(mock_remove_favorite):
#     """Тест удаления несуществующего фильма из избранного"""
#     mock_remove_favorite.return_value = False
    
#     client = TestClient(app)
#     response = client.delete(
#         "/favorites/films/999",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 404
#     assert "Not in favorites" in response.json()["detail"]


# @patch('app.routers.favorites.get_favorite_films')
# def test_list_favorite_films_success(mock_get_favorites):
#     """Тест получения списка избранных фильмов"""
#     mock_films = [
#         AsyncMock(film_id=1, title="Favorite Film 1"),
#         AsyncMock(film_id=2, title="Favorite Film 2")
#     ]
#     mock_get_favorites.return_value = mock_films
    
#     client = TestClient(app)
#     response = client.get(
#         "/favorites/films",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["count"] == 2
#     assert data["items"][0]["film_id"] == 1
#     assert data["items"][0]["title"] == "Favorite Film 1"


# --------------------------
# Тесты для избранных актеров
# --------------------------

# @patch('app.routers.favorites.add_favorite_actor')
# def test_add_favorite_actor_success(mock_add_favorite):
#     """Тест успешного добавления актера в избранное"""
#     mock_add_favorite.return_value = None
    
#     client = TestClient(app)
#     response = client.post(
#         "/favorites/actors/actor1",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["status"] == "added"
#     assert data["actor_id"] == "actor1"


# @patch('app.routers.favorites.remove_favorite_actor')
# def test_remove_favorite_actor_success(mock_remove_favorite):
#     """Тест успешного удаления актера из избранного"""
#     mock_remove_favorite.return_value = True
    
#     client = TestClient(app)
#     response = client.delete(
#         "/favorites/actors/actor1",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["status"] == "removed"
#     assert data["actor_id"] == "actor1"


# @patch('app.routers.favorites.remove_favorite_actor')
# def test_remove_favorite_actor_not_found(mock_remove_favorite):
#     """Тест удаления несуществующего актера из избранного"""
#     mock_remove_favorite.return_value = False
    
#     client = TestClient(app)
#     response = client.delete(
#         "/favorites/actors/nonexistent",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 404
#     assert "Not in favorites" in response.json()["detail"]


# @patch('app.routers.favorites.get_favorite_actors')
# def test_list_favorite_actors_success(mock_get_favorites):
#     """Тест получения списка избранных актеров"""
#     mock_actors = [
#         AsyncMock(actor_id="actor1", name="Actor One"),
#         AsyncMock(actor_id="actor2", name="Actor Two")
#     ]
#     mock_get_favorites.return_value = mock_actors
    
#     client = TestClient(app)
#     response = client.get(
#         "/favorites/actors",
#         headers=create_auth_headers()
#     )
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["count"] == 2
#     assert data["items"][0]["actor_id"] == "actor1"
#     assert data["items"][0]["name"] == "Actor One"
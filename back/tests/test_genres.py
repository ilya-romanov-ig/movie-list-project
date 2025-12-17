# tests/test_genres.py
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


# @patch('app.routers.genres.list_genres')
# def test_get_all_genres(mock_list_genres):
#     """Тест получения всех жанров"""
#     mock_genres = [
#         AsyncMock(genre_id=1, name="Action"),
#         AsyncMock(genre_id=2, name="Drama")
#     ]
#     mock_list_genres.return_value = mock_genres
    
#     client = TestClient(app)
#     response = client.get("/genres")
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["count"] == 2
#     assert data["items"][0]["genre_id"] == 1
#     assert data["items"][0]["name"] == "Action"


# @patch('app.routers.genres.list_genres')
# def test_get_all_genres_with_pagination(mock_list_genres):
#     """Тест получения жанров с пагинацией"""
#     mock_genres = [AsyncMock(genre_id=1, name="Action")]
#     mock_list_genres.return_value = mock_genres
    
#     client = TestClient(app)
#     response = client.get("/genres?limit=10&offset=0")
    
#     assert response.status_code == 200
#     mock_list_genres.assert_called_once()
#     call_kwargs = mock_list_genres.call_args[1]
#     assert call_kwargs["limit"] == 10
#     assert call_kwargs["offset"] == 0


# @patch('app.routers.genres.list_genres')
# def test_get_all_genres_with_search(mock_list_genres):
#     """Тест поиска жанров по имени"""
#     mock_genres = [AsyncMock(genre_id=1, name="Action")]
#     mock_list_genres.return_value = mock_genres
    
#     client = TestClient(app)
#     response = client.get("/genres?name=act")
    
#     assert response.status_code == 200
#     mock_list_genres.assert_called_once()
#     call_kwargs = mock_list_genres.call_args[1]
#     assert call_kwargs["name_query"] == "act"


# @patch('app.routers.genres.get_genre_by_id')
# def test_get_genre_success(mock_get_genre):
#     """Тест успешного получения жанра"""
#     mock_genre = AsyncMock(genre_id=1, name="Action")
#     mock_get_genre.return_value = mock_genre
    
#     client = TestClient(app)
#     response = client.get("/genres/1")
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["genre_id"] == 1
#     assert data["name"] == "Action"


@patch('app.routers.genres.get_genre_by_id')
def test_get_genre_not_found(mock_get_genre):
    """Тест получения несуществующего жанра"""
    mock_get_genre.return_value = None
    
    client = TestClient(app)
    response = client.get("/genres/999")
    
    assert response.status_code == 404
    assert "Genre not found" in response.json()["detail"]


@patch('app.routers.genres.get_films_of_genre')
def test_get_genre_films(mock_get_films):
    """Тест получения фильмов жанра"""
    mock_films = [
        AsyncMock(film_id=1, title="Film 1"),
        AsyncMock(film_id=2, title="Film 2")
    ]
    mock_get_films.return_value = mock_films
    
    client = TestClient(app)
    response = client.get("/genres/1/films")
    
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["items"][0]["film_id"] == 1
    assert data["items"][0]["title"] == "Film 1"


@patch('app.routers.genres.create_genre')
def test_create_genre_success(mock_create_genre):
    """Тест успешного создания жанра"""
    mock_genre = AsyncMock(genre_id=1, name="New Genre")
    mock_create_genre.return_value = mock_genre
    
    client = TestClient(app)
    response = client.post(
        "/genres",
        json={"name": "New Genre"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "created"
    assert data["genre_id"] == 1


def test_create_genre_missing_name():
    """Тест создания жанра без имени"""
    client = TestClient(app)
    response = client.post(
        "/genres",
        json={}
    )
    
    assert response.status_code == 400
    assert "Field 'name' is required" in response.json()["detail"]


@patch('app.routers.genres.update_genre')
def test_update_genre_success(mock_update_genre):
    """Тест успешного обновления жанра"""
    mock_genre = AsyncMock(genre_id=1, name="Updated Genre")
    mock_update_genre.return_value = mock_genre
    
    client = TestClient(app)
    response = client.patch(
        "/genres/1",
        json={"name": "Updated Genre"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "updated"


@patch('app.routers.genres.update_genre')
def test_update_genre_not_found(mock_update_genre):
    """Тест обновления несуществующего жанра"""
    mock_update_genre.return_value = None
    
    client = TestClient(app)
    response = client.patch(
        "/genres/999",
        json={"name": "Updated Genre"}
    )
    
    assert response.status_code == 404
    assert "Genre not found" in response.json()["detail"]


@patch('app.routers.genres.delete_genre')
def test_delete_genre_success(mock_delete_genre):
    """Тест успешного удаления жанра"""
    mock_delete_genre.return_value = True
    
    client = TestClient(app)
    response = client.delete("/genres/1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "deleted"


@patch('app.routers.genres.delete_genre')
def test_delete_genre_not_found(mock_delete_genre):
    """Тест удаления несуществующего жанра"""
    mock_delete_genre.return_value = False
    
    client = TestClient(app)
    response = client.delete("/genres/999")
    
    assert response.status_code == 404
    assert "Genre not found" in response.json()["detail"]
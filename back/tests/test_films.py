# tests/test_films.py
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app


@pytest.fixture
def mock_db():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def client():
    return TestClient(app)


# --------------------------
# Тесты для /films/top
# --------------------------
@patch('app.routers.films.get_top_by_rating')
def test_top_films(mock_get_top):
    """Тест получения топ фильмов по рейтингу"""
    mock_get_top.return_value = [
        MagicMock(film_id=1, title="Film 1"),
        MagicMock(film_id=2, title="Film 2")
    ]
    
    client = TestClient(app)
    response = client.get("/films/top")
    
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["items"][0]["id"] == 1
    assert data["items"][0]["title"] == "Film 1"


@patch('app.routers.films.get_top_by_rating')
def test_top_films_empty(mock_get_top):
    """Тест пустого списка топ фильмов"""
    mock_get_top.return_value = []
    
    client = TestClient(app)
    response = client.get("/films/top")
    
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["items"] == []


# --------------------------
# Тесты для /films/newest
# --------------------------
@patch('app.routers.films.get_newest')
def test_newest_films(mock_get_newest):
    """Тест получения новейших фильмов"""
    mock_get_newest.return_value = [
        MagicMock(film_id=3, title="New Film 1"),
        MagicMock(film_id=4, title="New Film 2")
    ]
    
    client = TestClient(app)
    response = client.get("/films/newest")
    
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["items"][0]["id"] == 3


# --------------------------
# Тесты для /films/{film_id}
# --------------------------
@patch('app.routers.films.get_film_by_id')
def test_film_details_success(mock_get_film):
    """Тест успешного получения деталей фильма"""
    mock_film = MagicMock(
        film_id=1,
        title="Test Film",
        year=2023,
        description="Test description",
        runtime=120,
        poster_url="http://example.com/poster.jpg"
    )
    mock_get_film.return_value = mock_film
    
    client = TestClient(app)
    response = client.get("/films/1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Film"
    assert data["year"] == 2023
    assert data["description"] == "Test description"


@patch('app.routers.films.get_film_by_id')
def test_film_details_not_found(mock_get_film):
    """Тест получения несуществующего фильма"""
    mock_get_film.return_value = None
    
    client = TestClient(app)
    response = client.get("/films/999")
    
    assert response.status_code == 404
    assert "Film not found" in response.json()["detail"]


# --------------------------
# Тесты для /films/{film_id}/actors
# --------------------------
# @patch('app.routers.films.get_actors_for_film')
# def test_film_actors(mock_get_actors):
#     """Тест получения актеров фильма"""
#     mock_actors = [
#         MagicMock(actor_id=1, name="Actor 1"),
#         MagicMock(actor_id=2, name="Actor 2")
#     ]
#     mock_get_actors.return_value = mock_actors
    
#     client = TestClient(app)
#     response = client.get("/films/1/actors")
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["count"] == 2
#     assert data["items"][0]["actor_id"] == 1
#     assert data["items"][0]["name"] == "Actor 1"


@patch('app.routers.films.get_actors_for_film')
def test_film_actors_empty(mock_get_actors):
    """Тест пустого списка актеров"""
    mock_get_actors.return_value = []
    
    client = TestClient(app)
    response = client.get("/films/1/actors")
    
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["items"] == []


# --------------------------
# Тесты для /films/{film_id}/genres
# --------------------------
# @patch('app.routers.films.get_genres_for_film')
# def test_film_genres(mock_get_genres):
#     """Тест получения жанров фильма"""
#     mock_genres = [
#         MagicMock(genre_id=1, name="Action"),
#         MagicMock(genre_id=2, name="Drama")
#     ]
#     mock_get_genres.return_value = mock_genres
    
#     client = TestClient(app)
#     response = client.get("/films/1/genres")
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["count"] == 2
#     assert data["items"][0]["genre_id"] == 1
#     assert data["items"][0]["name"] == "Action"


# --------------------------
# Тесты для /films/{film_id}/ratings
# --------------------------
@patch('app.routers.films.get_ratings_for_film')
def test_film_ratings(mock_get_ratings):
    """Тест получения рейтингов фильма"""
    mock_ratings = [
        MagicMock(user_id=1, rating=8),
        MagicMock(user_id=2, rating=9)
    ]
    mock_get_ratings.return_value = mock_ratings
    
    client = TestClient(app)
    response = client.get("/films/1/ratings")
    
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["items"][0]["user_id"] == 1
    assert data["items"][0]["rating"] == 8


# --------------------------
# Тесты для /films/{film_id}/rating
# --------------------------
@patch('app.routers.films.get_avg_rating')
def test_film_avg_rating(mock_get_avg):
    """Тест получения среднего рейтинга"""
    mock_get_avg.return_value = 8.5
    
    client = TestClient(app)
    response = client.get("/films/1/rating")
    
    assert response.status_code == 200
    data = response.json()
    assert data["film_id"] == 1
    assert data["avg_rating"] == 8.5


@patch('app.routers.films.get_avg_rating')
def test_film_avg_rating_none(mock_get_avg):
    """Тест получения среднего рейтинга (нет рейтингов)"""
    mock_get_avg.return_value = None
    
    client = TestClient(app)
    response = client.get("/films/1/rating")
    
    assert response.status_code == 200
    data = response.json()
    assert data["film_id"] == 1
    assert data["avg_rating"] is None


# --------------------------
# Тесты для /films/{film_id}/details
# --------------------------
@patch('app.routers.films.get_film_by_id')
@patch('app.routers.films.get_actors_for_film')
@patch('app.routers.films.get_genres_for_film')
@patch('app.routers.films.get_film_stats')
def test_film_details_comprehensive(mock_get_stats, mock_get_genres, mock_get_actors, mock_get_film):
    """Тест получения полных деталей фильма"""
    mock_film = MagicMock(
        film_id=1,
        title="Test Film",
        year=2023,
        description="Test description",
        runtime=120,
        poster_url="http://example.com/poster.jpg"
    )
    mock_get_film.return_value = mock_film
    
    mock_actors = [MagicMock(actor_id=1, name="Actor 1")]
    mock_get_actors.return_value = mock_actors
    
    mock_genres = [MagicMock(genre_id=1, name="Action")]
    mock_get_genres.return_value = mock_genres
    
    mock_stats = MagicMock(
        avg_rating=8.5,
        n_ratings=100,
        watched_count=500,
        updated_at="2024-01-01T00:00:00"
    )
    mock_get_stats.return_value = mock_stats
    
    client = TestClient(app)
    response = client.get("/films/1/details")
    
    assert response.status_code == 200
    data = response.json()
    assert data["film_id"] == 1
    assert data["title"] == "Test Film"
    assert len(data["actors"]) == 1
    assert len(data["genres"]) == 1
    assert data["stats"]["avg_rating"] == 8.5
    assert data["stats"]["ratings_count"] == 100


@patch('app.routers.films.get_film_by_id')
def test_film_details_comprehensive_not_found(mock_get_film):
    """Тест получения несуществующих деталей фильма"""
    mock_get_film.return_value = None
    
    client = TestClient(app)
    response = client.get("/films/999/details")
    
    assert response.status_code == 404
    assert "Film not found" in response.json()["detail"]
# tests/test_search.py
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


# @patch('app.routers.search.search_films')
# @patch('app.routers.search.search_actors')
# @patch('app.routers.search.search_users')
# def test_global_search_success(mock_search_users, mock_search_actors, mock_search_films):
#     """Тест успешного глобального поиска"""
#     mock_films = [
#         AsyncMock(film_id=1, title="Test Film"),
#         AsyncMock(film_id=2, title="Another Film")
#     ]
#     mock_search_films.return_value = mock_films
    
#     mock_actors = [
#         AsyncMock(actor_id="actor1", name="Test Actor")
#     ]
#     mock_search_actors.return_value = mock_actors
    
#     mock_users = [
#         AsyncMock(user_id=1, username="testuser")
#     ]
#     mock_search_users.return_value = mock_users
    
#     client = TestClient(app)
#     response = client.get("/search/?q=test")
    
#     assert response.status_code == 200
#     data = response.json()
    
#     assert data["query"] == "test"
#     assert len(data["results"]["films"]) == 2
#     assert len(data["results"]["actors"]) == 1
#     assert len(data["results"]["users"]) == 1
    
#     assert data["results"]["films"][0]["id"] == 1
#     assert data["results"]["films"][0]["title"] == "Test Film"
#     assert data["results"]["actors"][0]["id"] == "actor1"
#     assert data["results"]["actors"][0]["name"] == "Test Actor"
#     assert data["results"]["users"][0]["id"] == 1
#     assert data["results"]["users"][0]["username"] == "testuser"


@patch('app.routers.search.search_films')
@patch('app.routers.search.search_actors')
@patch('app.routers.search.search_users')
def test_global_search_empty(mock_search_users, mock_search_actors, mock_search_films):
    """Тест поиска без результатов"""
    mock_search_films.return_value = []
    mock_search_actors.return_value = []
    mock_search_users.return_value = []
    
    client = TestClient(app)
    response = client.get("/search/?q=nonexistent")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["query"] == "nonexistent"
    assert len(data["results"]["films"]) == 0
    assert len(data["results"]["actors"]) == 0
    assert len(data["results"]["users"]) == 0


def test_global_search_missing_query():
    """Тест поиска без query параметра"""
    client = TestClient(app)
    response = client.get("/search/")
    
    # FastAPI вернет 422 из-за отсутствия обязательного параметра
    assert response.status_code == 422


@patch('app.routers.search.search_films')
@patch('app.routers.search.search_actors')
@patch('app.routers.search.search_users')
def test_global_search_only_films(mock_search_users, mock_search_actors, mock_search_films):
    """Тест поиска, возвращающего только фильмы"""
    mock_films = [AsyncMock(film_id=1, title="Film Only")]
    mock_search_films.return_value = mock_films
    mock_search_actors.return_value = []
    mock_search_users.return_value = []
    
    client = TestClient(app)
    response = client.get("/search/?q=film")
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["results"]["films"]) == 1
    assert len(data["results"]["actors"]) == 0
    assert len(data["results"]["users"]) == 0
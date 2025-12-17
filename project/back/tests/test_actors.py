# tests/test_actors.py
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


# @patch('app.routers.actors.list_actors')
# def test_get_all_actors(mock_list_actors):
#     """Тест получения всех актеров"""
#     mock_actors = [
#         AsyncMock(actor_id="actor1", name="Actor One"),
#         AsyncMock(actor_id="actor2", name="Actor Two")
#     ]
#     mock_list_actors.return_value = mock_actors
    
#     client = TestClient(app)
#     response = client.get("/actors")
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["count"] == 2
#     assert data["items"][0]["actor_id"] == "actor1"
#     assert data["items"][0]["name"] == "Actor One"


# @patch('app.routers.actors.get_actor_by_id')
# def test_get_actor_success(mock_get_actor):
#     """Тест успешного получения актера"""
#     mock_actor = AsyncMock(
#         actor_id="actor1",
#         name="John Doe",
#         birth_year=1980,
#         bio="A great actor",
#         photo_url="http://example.com/photo.jpg"
#     )
#     mock_get_actor.return_value = mock_actor
    
#     client = TestClient(app)
#     response = client.get("/actors/actor1")
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["actor_id"] == "actor1"
#     assert data["name"] == "John Doe"
#     assert data["birth_year"] == 1980
#     assert data["bio"] == "A great actor"
#     assert data["photo_url"] == "http://example.com/photo.jpg"


@patch('app.routers.actors.get_actor_by_id')
def test_get_actor_not_found(mock_get_actor):
    """Тест получения несуществующего актера"""
    mock_get_actor.return_value = None
    
    client = TestClient(app)
    response = client.get("/actors/nonexistent")
    
    assert response.status_code == 404
    assert "Actor not found" in response.json()["detail"]


@patch('app.routers.actors.get_films_of_actor')
def test_get_actor_films(mock_get_films):
    """Тест получения фильмов актера"""
    mock_films = [
        AsyncMock(film_id=1, title="Film 1"),
        AsyncMock(film_id=2, title="Film 2")
    ]
    mock_get_films.return_value = mock_films
    
    client = TestClient(app)
    response = client.get("/actors/actor1/films")
    
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["items"][0]["film_id"] == 1
    assert data["items"][0]["title"] == "Film 1"


@patch('app.routers.actors.create_actor')
def test_create_actor_success(mock_create_actor):
    """Тест успешного создания актера"""
    mock_actor = AsyncMock(actor_id="new_actor")
    mock_create_actor.return_value = mock_actor
    
    client = TestClient(app)
    response = client.post(
        "/actors",
        json={
            "name": "New Actor",
            "bio": "New actor bio",
            "birth_year": 1990,
            "photo_url": "http://example.com/photo.jpg"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "created"
    assert data["actor_id"] == "new_actor"


def test_create_actor_missing_name():
    """Тест создания актера без имени"""
    client = TestClient(app)
    response = client.post(
        "/actors",
        json={
            "bio": "Some bio",
            "birth_year": 1990
        }
    )
    
    assert response.status_code == 400
    assert "Field 'name' is required" in response.json()["detail"]


@patch('app.routers.actors.update_actor')
def test_update_actor_success(mock_update_actor):
    """Тест успешного обновления актера"""
    mock_actor = AsyncMock(actor_id="actor1")
    mock_update_actor.return_value = mock_actor
    
    client = TestClient(app)
    response = client.patch(
        "/actors/actor1",
        json={
            "name": "Updated Name",
            "bio": "Updated bio"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "updated"


@patch('app.routers.actors.update_actor')
def test_update_actor_not_found(mock_update_actor):
    """Тест обновления несуществующего актера"""
    mock_update_actor.return_value = None
    
    client = TestClient(app)
    response = client.patch(
        "/actors/nonexistent",
        json={"name": "Updated Name"}
    )
    
    assert response.status_code == 404
    assert "Actor not found" in response.json()["detail"]


@patch('app.routers.actors.delete_actor')
def test_delete_actor_success(mock_delete_actor):
    """Тест успешного удаления актера"""
    mock_delete_actor.return_value = True
    
    client = TestClient(app)
    response = client.delete("/actors/actor1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "deleted"


@patch('app.routers.actors.delete_actor')
def test_delete_actor_not_found(mock_delete_actor):
    """Тест удаления несуществующего актера"""
    mock_delete_actor.return_value = False
    
    client = TestClient(app)
    response = client.delete("/actors/nonexistent")
    
    assert response.status_code == 404
    assert "Actor not found" in response.json()["detail"]
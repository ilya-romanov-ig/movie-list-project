# tests/test_home.py
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


# @patch('app.routers.home.get_top_by_rating')
# @patch('app.routers.home.get_newest')
# def test_home_page_unauthenticated(mock_get_newest, mock_get_top):
#     """Тест главной страницы без авторизации"""
#     mock_top_films = [
#         AsyncMock(film_id=1, title="Top Film 1", poster_url="url1", year=2023),
#         AsyncMock(film_id=2, title="Top Film 2", poster_url="url2", year=2022)
#     ]
#     mock_get_top.return_value = mock_top_films
    
#     mock_newest_films = [
#         AsyncMock(film_id=3, title="New Film 1", poster_url="url3", year=2024),
#         AsyncMock(film_id=4, title="New Film 2", poster_url="url4", year=2024)
#     ]
#     mock_get_newest.return_value = mock_newest_films
    
#     client = TestClient(app)
#     response = client.get("/home")
    
#     # Может быть 200 или 401 в зависимости от настроек get_optional_user
#     assert response.status_code in [200, 401]
    
#     if response.status_code == 200:
#         data = response.json()
#         assert "top_films" in data
#         assert "newest_films" in data
#         assert "recommended" in data
#         assert "trending" in data
#         assert len(data["top_films"]["items"]) == 2
#         assert len(data["newest_films"]["items"]) == 2


# @patch('app.routers.home.get_top_by_rating')
# @patch('app.routers.home.get_newest')
# @patch('app.routers.home.get_ml_recommendations')
# @patch('app.routers.home.get_films_by_ids')
# def test_home_page_authenticated_with_ml(mock_get_films, mock_get_ml, mock_get_newest, mock_get_top):
#     """Тест главной страницы с авторизацией и ML рекомендациями"""
#     # Мокаем стандартные данные
#     mock_top_films = [
#         AsyncMock(film_id=1, title="Top Film", poster_url="url1", year=2023)
#     ]
#     mock_get_top.return_value = mock_top_films
    
#     mock_newest_films = [
#         AsyncMock(film_id=2, title="New Film", poster_url="url2", year=2024)
#     ]
#     mock_get_newest.return_value = mock_newest_films
    
#     # Мокаем ML рекомендации
#     mock_get_ml.return_value = [3, 4, 5]
    
#     mock_recommended_films = [
#         AsyncMock(film_id=3, title="ML Rec 1", poster_url="url3", year=2023),
#         AsyncMock(film_id=4, title="ML Rec 2", poster_url="url4", year=2022),
#         AsyncMock(film_id=5, title="ML Rec 3", poster_url="url5", year=2021)
#     ]
#     mock_get_films.return_value = mock_recommended_films
    
#     client = TestClient(app)
#     response = client.get("/home", headers=create_auth_headers())
    
#     assert response.status_code == 200
#     data = response.json()
    
#     assert "top_films" in data
#     assert "newest_films" in data
#     assert "recommended" in data
#     assert "trending" in data
    
#     assert len(data["top_films"]["items"]) == 1
#     assert len(data["newest_films"]["items"]) == 1
#     assert len(data["recommended"]["items"]) == 3
#     assert len(data["trending"]["items"]) == 1


# @patch('app.routers.home.get_top_by_rating')
# @patch('app.routers.home.get_newest')
# @patch('app.routers.home.get_ml_recommendations')
# def test_home_page_authenticated_ml_fallback(mock_get_ml, mock_get_newest, mock_get_top):
#     """Тест главной страницы с fallback при недоступности ML"""
#     mock_top_films = [
#         AsyncMock(film_id=1, title="Top Film", poster_url="url1", year=2023),
#         AsyncMock(film_id=2, title="Top Film 2", poster_url="url2", year=2022),
#         AsyncMock(film_id=3, title="Top Film 3", poster_url="url3", year=2021),
#         AsyncMock(film_id=4, title="Top Film 4", poster_url="url4", year=2020),
#         AsyncMock(film_id=5, title="Top Film 5", poster_url="url5", year=2019),
#         AsyncMock(film_id=6, title="Top Film 6", poster_url="url6", year=2018),
#         AsyncMock(film_id=7, title="Top Film 7", poster_url="url7", year=2017),
#         AsyncMock(film_id=8, title="Top Film 8", poster_url="url8", year=2016)
#     ]
#     mock_get_top.return_value = mock_top_films
    
#     mock_newest_films = [
#         AsyncMock(film_id=9, title="New Film", poster_url="url9", year=2024)
#     ]
#     mock_get_newest.return_value = mock_newest_films
    
#     # ML возвращает пустой список (fallback)
#     mock_get_ml.return_value = []
    
#     client = TestClient(app)
#     response = client.get("/home", headers=create_auth_headers())
    
#     assert response.status_code == 200
#     data = response.json()
    
#     # Проверяем, что recommended заполнено топовыми фильмами (fallback)
#     assert len(data["recommended"]["items"]) > 0


# @patch('app.routers.home.get_ml_recommendations')
# @patch('app.routers.home.get_films_by_ids')
# def test_recommended_endpoint(mock_get_films, mock_get_ml):
#     """Тест эндпоинта /home/recommended"""
#     # Мокаем ML рекомендации
#     mock_get_ml.return_value = [1, 2, 3]
    
#     mock_films = [
#         AsyncMock(film_id=1, title="Rec 1", poster_url="url1", year=2023),
#         AsyncMock(film_id=2, title="Rec 2", poster_url="url2", year=2022),
#         AsyncMock(film_id=3, title="Rec 3", poster_url="url3", year=2021)
#     ]
#     mock_get_films.return_value = mock_films
    
#     client = TestClient(app)
#     response = client.get("/home/recommended", headers=create_auth_headers())
    
#     assert response.status_code == 200
#     data = response.json()
    
#     assert "items" in data
#     assert "source" in data
#     assert data["source"] == "ml_service"
#     assert len(data["items"]) == 3


def test_recommended_endpoint_no_auth():
    """Тест эндпоинта /home/recommended без авторизации"""
    client = TestClient(app)
    response = client.get("/home/recommended")
    
    assert response.status_code == 401


# @patch('app.routers.home.get_top_by_rating')
# def test_trending_endpoint(mock_get_top):
#     """Тест эндпоинта /home/trending"""
#     mock_films = [
#         AsyncMock(film_id=1, title="Trending 1", poster_url="url1", year=2023),
#         AsyncMock(film_id=2, title="Trending 2", poster_url="url2", year=2022)
#     ]
#     mock_get_top.return_value = mock_films
    
#     client = TestClient(app)
#     response = client.get("/home/trending")
    
#     assert response.status_code == 200
#     data = response.json()
    
#     assert "items" in data
#     assert len(data["items"]) == 2
#     assert data["items"][0]["id"] == 1
#     assert data["items"][0]["title"] == "Trending 1"
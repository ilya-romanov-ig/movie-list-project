import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Минимальная конфигурация приложения"""
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    CACHE_TTL = int(os.getenv("CACHE_TTL", 300))  # 5 минут
    MODEL_UPDATE_INTERVAL = int(os.getenv("MODEL_UPDATE_INTERVAL", 3600))
    
    DATA_PATHS = {
        'ratings': os.getenv('RATINGS_PATH', 'data/ratings.csv'),
        'fav_films': os.getenv('FAV_FILMS_PATH', 'data/favorite_films.csv'),
        'fav_actors': os.getenv('FAV_ACTORS_PATH', 'data/favorite_actors.csv'),
        'film_actor': os.getenv('FILM_ACTOR_PATH', 'data/film_actors.csv'),
    }
    
    MODEL_PARAMS = {
        'time_decay_days': 90,
        'min_ratings_for_popular': 3,
        'trending_days': 30,
    }

config = Config()
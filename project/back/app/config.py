from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Настройки базы данных и аутентификации
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    
    # Настройки для изображений
    # Базовый URL API (для Docker: http://backend:8000, для localhost: http://localhost:8001)
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8001")
    
    # Путь к постерам в файловой системе
    POSTERS_PATH: str = os.getenv("POSTERS_PATH", "/app/posters")
    
    # URL для доступа к постерам через API
    POSTERS_BASE_URL: str = os.getenv("POSTERS_BASE_URL", f"{BASE_URL}/posters")

    class Config:
        env_file = ".env"

settings = Settings()
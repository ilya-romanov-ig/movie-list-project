# app/clients/ml_client.py
import httpx
import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)


class MLClient:
    def __init__(self):
        self.base_url = os.getenv("ML_URL", "http://movie-recommender:8000")
        logger.info(f"ML client initialized with URL: {self.base_url}")
        
        # Создаем клиент только при необходимости
        self._client = None
    
    @property
    def client(self):
        """Ленивая инициализация клиента"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(connect=5.0, read=30.0, write=5.0)
            )
        return self._client
    
    async def get_recommendations(self, user_id: int, count: int = 10) -> List[int]:
        """Получить рекомендации от ML-сервиса"""
        try:
            url = f"{self.base_url}/recommend/{user_id}"
            logger.info(f"Requesting recommendations from: {url}")
            
            # Используем property client
            response = await self.client.get(url, params={"count": count})
            response.raise_for_status()
            data = response.json()
            recommendations = data.get("recommendations", [])
            
            # Преобразуем в обычные int на всякий случай
            return [int(item) for item in recommendations if isinstance(item, (int, float))]
            
        except httpx.HTTPStatusError as e:
            logger.error(f"ML сервис вернул ошибку {e.response.status_code}")
            return []
        except Exception as e:
            logger.error(f"Ошибка подключения к ML сервису: {e}")
            return []
    
    async def health_check(self) -> bool:
        """Проверить доступность ML-сервиса"""
        try:
            response = await self.client.get(f"{self.base_url}/health", timeout=5.0)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"ML health check failed: {e}")
            return False
    
    async def close(self):
        """Закрыть клиент"""
        if self._client:
            await self._client.aclose()


# Создаем экземпляр
ml_client = MLClient()
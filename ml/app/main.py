from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
from typing import Optional
import logging

from .recommender import MovieRecommender
from .config import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Movie Recommender API",
    description="Простая система рекомендаций фильмов",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация рекоммендера
try:
    recommender = MovieRecommender(config.DATA_PATHS)
    logger.info(f"Рекоммендер инициализирован. Данные загружены: {not recommender.ratings.empty}")
except Exception as e:
    logger.error(f"Ошибка инициализации рекоммендера: {e}")
    recommender = None

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "service": "Movie Recommender",
        "version": "1.0.0",
        "status": "running",
        "data_loaded": not recommender.ratings.empty if recommender else False
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    if not recommender:
        raise HTTPException(status_code=500, detail="Recommender not initialized")
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "data_rows": len(recommender.ratings) if not recommender.ratings.empty else 0,
        "last_update": recommender.last_update.isoformat()
    }

@app.get("/recommend/{user_id}")
async def get_recommendations(
    user_id: int,
    count: Optional[int] = Query(10, ge=1, le=50),
    explain: Optional[bool] = False
):
    """Получить рекомендации для пользователя"""
    try:
        if not recommender:
            raise HTTPException(status_code=500, detail="Recommender not initialized")
        
        recommendations = recommender.get_recommendations(user_id, count)
        
        response = {
            "user_id": user_id,
            "recommendations": recommendations,
            "count": len(recommendations),
            "timestamp": datetime.now().isoformat(),
            "engagement_level": recommender._get_user_engagement_level(user_id)
        }
        
        if explain and recommendations:
            explanation = []
            if len(recommendations) > 0:
                explanation.append(f"На основе ваших предпочтений и популярных фильмов")
            response["explanation"] = explanation
        
        return response
    
    except Exception as e:
        logger.error(f"Ошибка получения рекомендаций: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refresh")
async def refresh_data(background_tasks: BackgroundTasks):
    """Принудительное обновление данных"""
    def update_in_background():
        try:
            recommender.update_data()
            logger.info("Данные успешно обновлены")
        except Exception as e:
            logger.error(f"Ошибка обновления данных: {e}")
    
    background_tasks.add_task(update_in_background)
    
    return {
        "status": "update_started",
        "message": "Data refresh initiated in background",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/action")
async def log_action(
    user_id: int,
    action_type: str = Query(..., regex="^(rate|fav_film|fav_actor)$"),
    item_id: int = Query(...),
    rating: Optional[float] = Query(None, ge=0, le=5)
):
    """Записать действие пользователя"""
    try:
        if not recommender:
            raise HTTPException(status_code=500, detail="Recommender not initialized")
        
        if action_type == 'rate' and rating is None:
            raise HTTPException(status_code=400, detail="Rating is required for action_type='rate'")
        
        recommender.update_user_preferences(user_id, action_type, item_id, rating)
        
        return {
            "status": "success",
            "message": f"Action '{action_type}' logged successfully",
            "user_id": user_id,
            "item_id": item_id,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Ошибка записи действия: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.ENVIRONMENT == "development"
    )
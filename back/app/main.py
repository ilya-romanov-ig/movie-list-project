# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import os
from app.config import settings

app = FastAPI(
    title="Movies API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Упрощаем CORS настройки
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8001",  # Добавляем порт 8001
    "http://127.0.0.1:8001",  # Добавляем порт 8001
]

@app.middleware("http")
async def options_middleware(request, call_next):
    if request.method == "OPTIONS":
        # Возвращаем успешный ответ для OPTIONS
        response = JSONResponse(
            status_code=200,
            content={"status": "ok"},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Max-Age": "600",
            }
        )
        return response
    
    # Продолжаем обычную обработку для других методов
    response = await call_next(request)
    return response

# Устанавливаем CORS как первый middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

# Добавляем GZip сжатие
app.add_middleware(GZipMiddleware, minimum_size=1000)


os.makedirs(settings.POSTERS_PATH, exist_ok=True)
app.mount("/posters", StaticFiles(directory=settings.POSTERS_PATH), name="posters")

from app.routers import (
    films,
    actors,
    users,
    auth,
    favorites,
    ratings,
    watched,
    search,
    home,
    genres,
)


# Убираем кастомный middleware и OPTIONS handler - 
# FastAPI CORSMiddleware сам обрабатывает OPTIONS

# Подключение роутеров
app.include_router(auth.router)
app.include_router(films.router)
app.include_router(actors.router)
app.include_router(users.router)
app.include_router(favorites.router)
app.include_router(ratings.router)
app.include_router(watched.router)
app.include_router(search.router)
app.include_router(home.router)
app.include_router(genres.router)

# Корневой endpoint
@app.get("/")
async def root():
    return {
        "message": "Movies API",
        "docs": "/api/docs",
        "health": "/health"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "movies-api"}
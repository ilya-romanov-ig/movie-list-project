@echo off
echo ========================================
echo Movie Recommender Desktop Launcher
echo ========================================

REM Проверяем Docker
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ ERROR: Docker не установлен!
    echo Установите Docker Desktop с https://docker.com
    pause
    exit /b 1
)

REM Проверяем Docker Compose
where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ ERROR: Docker Compose не установлен!
    pause
    exit /b 1
)

echo ✅ Docker и Docker Compose доступны

echo.
echo 🚀 Запуск Docker сервисов...
echo Пожалуйста, подождите...

cd /d "%~dp0..\project"
docker-compose up -d

if %errorlevel% neq 0 (
    echo ❌ Ошибка запуска Docker сервисов
    echo Попробуйте запустить вручную:
    echo cd project
    echo docker-compose up -d
    pause
    exit /b 1
)

echo ✅ Docker сервисы запущены
echo.

echo ⏳ Ожидание запуска сервисов (10 секунд)...
timeout /t 10 /nobreak >nul

echo.
echo 🖥️ Запуск десктопного приложения...
cd /d "%~dp0"
start "" "movie-recommender-desktop.exe"

echo.
echo ✅ Приложение запущено!
echo Сервисы доступны по адресам:
echo • Vue приложение: http://localhost:5173
echo • FastAPI бэкенд: http://localhost:8001
echo • ML сервис: http://localhost:8002
echo • API документация: http://localhost:8001/docs
echo.
echo Для остановки сервисов выполните:
echo docker-compose down
pause
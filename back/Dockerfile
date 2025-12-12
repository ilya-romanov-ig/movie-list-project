FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt update && apt install -y \
    gcc \
    g++ \
    libpq-dev \
    build-essential \
    && apt clean && rm -rf /var/lib/apt/lists/*


RUN mkdir -p /app/posters
# Установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем ВСЮ папку app внутрь контейнера
COPY app/ ./app

EXPOSE 8000

# Запускаем из директории /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

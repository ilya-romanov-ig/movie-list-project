FROM python:3.11-alpine

WORKDIR /app

# Устанавливаем системные зависимости для Alpine
RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    python3-dev \
    py3-pip \
    libstdc++ \
    curl

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY app/ ./app/

# Создаем директории
RUN mkdir -p /app/data /app/logs

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
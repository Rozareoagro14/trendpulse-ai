# Инструкция по настройке TrendPulse AI на сервере

## 1. Подключение к серверу

```bash
ssh root@45.142.122.145
# Пароль: W5AV!54uq@5EMXLA
```

## 2. Переход в директорию проекта

```bash
cd /opt/trendpulse-ai
```

## 3. Проверка и исправление структуры файлов

```bash
# Проверяем структуру
ls -la
ls -la backend/
ls -la bot/

# Создаем недостающие файлы __init__.py
echo "# Backend module" > backend/__init__.py
echo "# Bot module" > bot/__init__.py

# Проверяем содержимое основных файлов
cat backend/main.py | head -10
cat bot/main.py | head -10
```

## 4. Обновление файла .env с правильным токеном

```bash
cat > .env << 'EOF'
# Telegram Bot Token
BOT_TOKEN=7997361131:AAHPvGAAAxwgu5RxQaUOoOvZT79Ig-u3_4w

# База данных
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/trendpulse

# Окружение
ENVIRONMENT=production

# API URL (для бота)
API_URL=http://backend:8000
EOF
```

## 5. Исправление Dockerfile для backend

```bash
cat > Dockerfile.backend << 'EOF'
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc g++ libpq-dev libffi-dev libssl-dev \
    libxml2-dev libxslt1-dev libjpeg-dev libpng-dev \
    libwebp-dev libcairo2-dev libpango1.0-dev \
    libgdk-pixbuf2.0-dev shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY .env* ./

RUN mkdir -p /app/reports /app/logs

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
```

## 6. Исправление Dockerfile для bot

```bash
cat > Dockerfile.bot << 'EOF'
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc g++ libpq-dev libffi-dev libssl-dev curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ ./bot/
COPY backend/ ./backend/
COPY .env* ./

RUN mkdir -p /app/logs

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["python", "bot/main.py"]
EOF
```

## 7. Обновление docker-compose.yml

```bash
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: trendpulse
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/trendpulse
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./reports:/app/reports
      - ./logs:/app/logs
    restart: unless-stopped

  bot:
    build:
      context: .
      dockerfile: Dockerfile.bot
    environment:
      - BOT_TOKEN=7997361131:AAHPvGAAAxwgu5RxQaUOoOvZT79Ig-u3_4w
      - API_URL=http://backend:8000
    depends_on:
      - backend
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

volumes:
  postgres_data:
EOF
```

## 8. Остановка старых контейнеров

```bash
docker-compose down
```

## 9. Очистка Docker

```bash
docker system prune -f
docker volume prune -f
```

## 10. Пересборка и запуск контейнеров

```bash
docker-compose up --build -d
```

## 11. Проверка статуса

```bash
docker-compose ps
```

## 12. Просмотр логов

```bash
docker-compose logs -f
```

## 13. Проверка работы API

```bash
curl http://localhost:8000/health
```

## 14. Проверка работы бота

Найдите бота в Telegram: @trendpulse_aiv2_bot
Отправьте команду `/start`

## Диагностика проблем

### Проверка содержимого контейнеров:
```bash
# Проверка backend контейнера
docker exec -it trendpulse-ai_backend_1 ls -la /app
docker exec -it trendpulse-ai_backend_1 ls -la /app/backend

# Проверка bot контейнера
docker exec -it trendpulse-ai_bot_1 ls -la /app
docker exec -it trendpulse-ai_bot_1 ls -la /app/bot
```

### Проверка логов конкретного сервиса:
```bash
docker-compose logs backend
docker-compose logs bot
```

### Перезапуск конкретного сервиса:
```bash
docker-compose restart backend
docker-compose restart bot
```

## Если проблемы остаются

1. Проверьте, что все файлы существуют:
```bash
ls -la backend/
ls -la bot/
```

2. Проверьте содержимое файлов:
```bash
head -5 backend/main.py
head -5 bot/main.py
```

3. Проверьте права доступа:
```bash
chmod -R 755 backend/
chmod -R 755 bot/
```

4. Пересоберите образы с нуля:
```bash
docker-compose down
docker system prune -af
docker-compose up --build -d
``` 
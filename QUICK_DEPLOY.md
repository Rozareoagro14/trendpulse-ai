# 🚀 Быстрое развертывание TrendPulse AI на сервере

## Подключение к серверу и развертывание

```bash
# 1. Подключение к серверу
ssh root@45.142.122.145
# Пароль: W5AV!54uq@5EMXLA

# 2. Установка Git (если не установлен)
apt update && apt install -y git

# 3. Очистка и клонирование (если директория уже существует)
rm -rf /opt/trendpulse-ai
mkdir -p /opt/trendpulse-ai
cd /opt/trendpulse-ai
git clone https://github.com/Rozareoagro14/trendpulse-ai.git .

# 4. Создание .env файла
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

# 5. Запуск развертывания
chmod +x deploy.sh
./deploy.sh
```

## Диагностика проблем

```bash
# Проверка логов backend (для перезапускающихся контейнеров)
docker-compose logs --tail=50 backend

# Проверка логов bot (для перезапускающихся контейнеров)
docker-compose logs --tail=50 bot

# Проверка статуса контейнеров
docker-compose ps

# Проверка логов всех сервисов
docker-compose logs --tail=20

# Остановка и перезапуск с логами
docker-compose down
docker-compose up --build
```

## Если контейнеры перезапускаются

```bash
# Проверьте логи для понимания причины
docker-compose logs backend | tail -20
docker-compose logs bot | tail -20

# Попробуйте запустить без фонового режима для просмотра ошибок
docker-compose down
docker-compose up --build

# Или запустите отдельные сервисы для диагностики
docker-compose up db -d
docker-compose up backend --build
```

## Если директория уже существует

```bash
# Вариант 1: Полная очистка и переустановка
rm -rf /opt/trendpulse-ai
mkdir -p /opt/trendpulse-ai
cd /opt/trendpulse-ai
git clone https://github.com/Rozareoagro14/trendpulse-ai.git .

# Вариант 2: Обновление существующего репозитория
cd /opt/trendpulse-ai
git fetch origin
git reset --hard origin/main
```

## Проверка работы

```bash
# Проверка статуса контейнеров
docker-compose ps

# Проверка API
curl http://localhost:8000/health

# Просмотр логов
docker-compose logs -f
```

## Обновление (после изменений в коде)

```bash
# На сервере
cd /opt/trendpulse-ai
./deploy.sh

# Или удаленно
ssh root@45.142.122.145 "cd /opt/trendpulse-ai && ./deploy.sh"
```

## Полезные команды

```bash
# Перезапуск сервисов
docker-compose restart

# Просмотр логов конкретного сервиса
docker-compose logs -f backend
docker-compose logs -f bot

# Остановка всех сервисов
docker-compose down

# Полная очистка и перезапуск
docker-compose down
docker system prune -f
docker-compose up --build -d
```

## Доступ к сервисам

- **API:** http://45.142.122.145:8000
- **Бот:** @trendpulse_aiv2_bot
- **Документация API:** http://45.142.122.145:8000/docs 
# 🚀 Руководство по развертыванию TrendPulse AI

## 📋 Обзор

TrendPulse AI - это система для девелоперов и строителей, состоящая из:
- **Backend API** (FastAPI)
- **Telegram Bot** (aiogram)
- **PostgreSQL Database**

## 🔧 Требования

- Docker и Docker Compose
- Git
- Доступ к серверу
- Telegram Bot Token

## 🏗️ Архитектура

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram Bot  │    │   FastAPI       │    │   PostgreSQL    │
│   (aiogram)     │◄──►│   Backend       │◄──►│   Database      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/Rozareoagro14/trendpulse-ai.git
cd trendpulse-ai
```

### 2. Создание .env файла
```bash
cat > .env << 'EOF'
# Telegram Bot
BOT_TOKEN=[ВАШ_ТОКЕН_БОТА]

# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/trendpulse

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
EOF
```

### 3. Запуск системы
```bash
docker-compose up -d
```

### 4. Проверка работы
```bash
# API
curl http://localhost:8000/health

# Bot
# Отправьте /start в Telegram
```

## 🔑 Получение токена бота

1. Откройте Telegram
2. Найдите @BotFather
3. Отправьте `/newbot`
4. Следуйте инструкциям:
   - Введите имя бота: `TrendPulse`
   - Введите username: `trendpulse_ai_bot`
5. Скопируйте полученный токен
6. Добавьте токен в `.env` файл

## 🐳 Docker Compose конфигурация

```yaml
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
    ports:
      - "5432:5432"

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/trendpulse
    ports:
      - "8000:8000"
    depends_on:
      - db

  bot:
    build:
      context: .
      dockerfile: Dockerfile.bot
    environment:
      - BOT_TOKEN=[ВАШ_ТОКЕН_БОТА]
      - API_URL=http://backend:8000
    depends_on:
      - backend

volumes:
  postgres_data:
```

## 📊 API Endpoints

### Основные endpoints:
- `GET /health` - Проверка здоровья
- `GET /api-info` - Информация об API
- `GET /projects/` - Список проектов
- `POST /projects/` - Создание проекта
- `GET /contractors/` - Список подрядчиков
- `GET /scenarios/` - Список сценариев

### Примеры запросов:
```bash
# Проверка здоровья
curl http://localhost:8000/health

# Создание проекта
curl -X POST http://localhost:8000/projects/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Жилой комплекс",
    "description": "Современный жилой комплекс",
    "project_type": "residential",
    "location": "Москва",
    "budget": 50000000,
    "area": 5000
  }'

# Получение проектов
curl http://localhost:8000/projects/

# Получение подрядчиков
curl http://localhost:8000/contractors/
```

## 🤖 Telegram Bot

### Команды:
- `/start` - Начало работы
- `/projects` - Мои проекты
- `/contractors` - Подрядчики
- `/scenarios` - Сценарии
- `/help` - Помощь

### Настройка:
1. Создайте бота через @BotFather
2. Получите токен
3. Добавьте токен в `.env`
4. Перезапустите контейнеры

## 🔍 Мониторинг и логи

### Просмотр логов:
```bash
# Все контейнеры
docker-compose logs

# Только backend
docker-compose logs backend

# Только bot
docker-compose logs bot

# Следить за логами
docker-compose logs -f
```

### Проверка статуса:
```bash
# Статус контейнеров
docker-compose ps

# Использование ресурсов
docker stats
```

## 🛠️ Устранение неполадок

### Проблема: Контейнеры не запускаются
```bash
# Проверьте логи
docker-compose logs

# Пересоберите образы
docker-compose build --no-cache

# Удалите volumes и пересоздайте
docker-compose down -v
docker-compose up -d
```

### Проблема: База данных не подключается
```bash
# Проверьте переменные окружения
docker-compose exec backend env | grep DATABASE

# Проверьте доступность базы
docker-compose exec backend ping db

# Проверьте логи базы
docker-compose logs db
```

### Проблема: Бот не отвечает
```bash
# Проверьте токен
docker-compose exec bot env | grep BOT_TOKEN

# Проверьте подключение к API
docker-compose exec bot ping backend

# Проверьте логи бота
docker-compose logs bot
```

### Проблема: API не отвечает
```bash
# Проверьте порты
netstat -tlnp | grep 8000

# Проверьте логи backend
docker-compose logs backend

# Перезапустите backend
docker-compose restart backend
```

## 📝 Полезные команды

```bash
# Остановка системы
docker-compose down

# Перезапуск
docker-compose restart

# Обновление кода
git pull
docker-compose build
docker-compose up -d

# Очистка Docker
docker system prune -a

# Резервное копирование базы
docker-compose exec db pg_dump -U postgres trendpulse > backup.sql

# Восстановление базы
docker-compose exec -T db psql -U postgres trendpulse < backup.sql

# Просмотр переменных окружения
docker-compose exec backend env
docker-compose exec bot env
```

## 🔒 Безопасность

### Рекомендации:
1. Измените пароли по умолчанию
2. Используйте HTTPS в продакшене
3. Ограничьте доступ к портам
4. Регулярно обновляйте зависимости
5. Мониторьте логи

### Переменные окружения для продакшена:
```env
DEBUG=false
LOG_LEVEL=INFO
SECRET_KEY=[СЛОЖНЫЙ_СЕКРЕТНЫЙ_КЛЮЧ]
DATABASE_URL=[ПРОДАКШЕН_URL_БАЗЫ]
BOT_TOKEN=[ВАШ_ТОКЕН_БОТА]
```

## 🚀 Развертывание на сервере

### 1. Подключение к серверу
```bash
ssh root@[IP_СЕРВЕРА]
# Пароль: [СКРЫТО]
```

### 2. Установка зависимостей
```bash
# Обновление системы
apt update && apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установка Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 3. Клонирование проекта
```bash
cd /opt
git clone https://github.com/Rozareoagro14/trendpulse-ai.git
cd trendpulse-ai
```

### 4. Создание .env файла
```bash
cat > .env << 'EOF'
BOT_TOKEN=[ВАШ_ТОКЕН_БОТА]
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/trendpulse
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
EOF
```

### 5. Запуск системы
```bash
docker-compose up -d
```

### 6. Проверка работы
```bash
# Проверка API
curl http://localhost:8000/health

# Проверка статуса контейнеров
docker-compose ps
```

## 🔄 Обновление системы

### Автоматическое обновление:
```bash
# Создайте скрипт обновления
cat > update.sh << 'EOF'
#!/bin/bash
cd /opt/trendpulse-ai
git pull
docker-compose build
docker-compose up -d
EOF

chmod +x update.sh
```

### Ручное обновление:
```bash
cd /opt/trendpulse-ai
git pull
docker-compose build
docker-compose up -d
```

## 📊 Мониторинг в продакшене

### Настройка логирования:
```bash
# Создание директории для логов
mkdir -p /opt/trendpulse-ai/logs

# Настройка ротации логов
cat > /etc/logrotate.d/trendpulse << 'EOF'
/opt/trendpulse-ai/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 root root
}
EOF
```

### Мониторинг ресурсов:
```bash
# Создание скрипта мониторинга
cat > monitor.sh << 'EOF'
#!/bin/bash
echo "=== TrendPulse AI Status ==="
echo "Date: $(date)"
echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "Memory: $(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2}')"
echo "Disk: $(df -h | awk '$NF=="/"{printf "%s", $5}')"
echo "=== Docker Status ==="
docker-compose ps
echo "=== API Health ==="
curl -s http://localhost:8000/health || echo "API недоступен"
EOF

chmod +x monitor.sh
```

## 🆘 Поддержка

### Полезные команды для диагностики:
```bash
# Проверка системы
docker system df
docker images
docker ps -a

# Проверка сети
docker network ls
docker network inspect trendpulse-ai_default

# Проверка volumes
docker volume ls
docker volume inspect trendpulse-ai_postgres_data

# Проверка логов
docker-compose logs --tail=100
```

### Контакты для поддержки:
- GitHub Issues: https://github.com/Rozareoagro14/trendpulse-ai/issues
- Документация: README.md

## 🎯 Следующие шаги

После успешного развертывания:
1. Настройте SSL сертификат
2. Настройте резервное копирование
3. Настройте мониторинг
4. Добавьте подрядчиков
5. Создайте первый проект 
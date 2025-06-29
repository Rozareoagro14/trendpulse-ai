# 🚀 Инструкции по настройке TrendPulse AI

## 📋 Требования
- Docker и Docker Compose
- Git
- Доступ к серверу

## 🔑 Доступ к серверу
- **IP:** trashy-leg
- **Пользователь:** root
- **Пароль:** [СКРЫТО]

## 📁 Структура проекта
```
trendpulse-ai/
├── backend/          # FastAPI backend
├── bot/             # Telegram bot
├── docker-compose.yml
├── .env             # Конфигурация (создать)
└── README.md
```

## 🔧 Настройка

### 1. Клонирование репозитория
```bash
git clone https://github.com/Rozareoagro14/trendpulse-ai.git
cd trendpulse-ai
```

### 2. Создание .env файла
Создайте файл `.env` в корне проекта:

```env
# Telegram Bot
BOT_TOKEN=[ВАШ_ТОКЕН_БОТА]

# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/trendpulse

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
```

### 3. Получение токена бота
1. Откройте Telegram
2. Найдите @BotFather
3. Отправьте `/newbot`
4. Следуйте инструкциям
5. Скопируйте полученный токен в `.env`

### 4. Запуск системы
```bash
# Сборка образов
docker-compose build

# Запуск контейнеров
docker-compose up -d

# Проверка статуса
docker-compose ps
```

### 5. Проверка работы
```bash
# Проверка API
curl http://localhost:8000/health

# Проверка бота
# Отправьте /start в Telegram боту
```

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
- `GET /health` - Проверка здоровья API
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
    "name": "Тестовый проект",
    "description": "Описание проекта",
    "project_type": "residential",
    "location": "Москва",
    "budget": 1000000,
    "area": 100
  }'
```

## 🤖 Telegram Bot

### Команды бота:
- `/start` - Начало работы
- `/projects` - Мои проекты
- `/contractors` - Подрядчики
- `/scenarios` - Сценарии
- `/help` - Помощь

### Настройка бота:
1. Создайте бота через @BotFather
2. Получите токен
3. Добавьте токен в `.env` файл
4. Перезапустите контейнеры

## 🔍 Мониторинг

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
```

### Проблема: Бот не отвечает
```bash
# Проверьте токен
docker-compose exec bot env | grep BOT_TOKEN

# Проверьте подключение к API
docker-compose exec bot ping backend
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
```

## 🔒 Безопасность

### Рекомендации:
1. Измените пароли по умолчанию
2. Используйте HTTPS в продакшене
3. Ограничьте доступ к портам
4. Регулярно обновляйте зависимости
5. Мониторьте логи на подозрительную активность

### Переменные окружения для продакшена:
```env
DEBUG=false
LOG_LEVEL=INFO
SECRET_KEY=[СЛОЖНЫЙ_СЕКРЕТНЫЙ_КЛЮЧ]
DATABASE_URL=[ПРОДАКШЕН_URL_БАЗЫ]
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи контейнеров
2. Убедитесь в корректности .env файла
3. Проверьте доступность всех сервисов
4. Обратитесь к документации API

## 🎯 Следующие шаги

После успешной настройки:
1. Создайте первый проект через бота
2. Добавьте подрядчиков
3. Сгенерируйте сценарии
4. Настройте мониторинг
5. Подготовьте к продакшену 
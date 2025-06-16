# Руководство по развертыванию TrendPulse AI через Git

## 1. Подготовка локального репозитория

### Инициализация Git репозитория
```bash
# В директории проекта
git init
git add .
git commit -m "Initial commit: TrendPulse AI MVP v3.0.0"
```

### Создание репозитория на GitHub/GitLab
1. Зайдите на GitHub.com или GitLab.com
2. Создайте новый репозиторий: `trendpulse-ai`
3. НЕ инициализируйте с README (у нас уже есть файлы)

### Привязка к удаленному репозиторию
```bash
# Замените YOUR_USERNAME на ваше имя пользователя
git remote add origin https://github.com/YOUR_USERNAME/trendpulse-ai.git
git branch -M main
git push -u origin main
```

## 2. Настройка сервера для автоматического развертывания

### Подключение к серверу
```bash
ssh root@45.142.122.145
# Пароль: W5AV!54uq@5EMXLA
```

### Установка Git на сервере
```bash
apt update
apt install -y git
```

### Создание директории для проекта
```bash
mkdir -p /opt/trendpulse-ai
cd /opt/trendpulse-ai
```

### Клонирование репозитория
```bash
# Замените YOUR_USERNAME на ваше имя пользователя
git clone https://github.com/YOUR_USERNAME/trendpulse-ai.git .
```

### Создание файла .env на сервере
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

## 3. Создание скрипта автоматического развертывания

### Создание скрипта deploy.sh
```bash
cat > /opt/trendpulse-ai/deploy.sh << 'EOF'
#!/bin/bash

echo "🚀 Начинаем развертывание TrendPulse AI..."

# Переходим в директорию проекта
cd /opt/trendpulse-ai

# Получаем последние изменения
echo "📥 Получаем последние изменения из Git..."
git pull origin main

# Останавливаем контейнеры
echo "🛑 Останавливаем контейнеры..."
docker-compose down

# Очищаем Docker
echo "🧹 Очищаем Docker..."
docker system prune -f

# Пересобираем и запускаем
echo "🔨 Пересобираем и запускаем контейнеры..."
docker-compose up --build -d

# Ждем запуска
echo "⏳ Ждем запуска сервисов..."
sleep 30

# Проверяем статус
echo "📊 Проверяем статус контейнеров..."
docker-compose ps

# Проверяем API
echo "🔍 Проверяем API..."
curl -f http://localhost:8000/health || echo "❌ API не отвечает"

echo "✅ Развертывание завершено!"
echo "🌐 API доступен по адресу: http://45.142.122.145:8000"
echo "🤖 Бот: @trendpulse_aiv2_bot"
EOF

# Делаем скрипт исполняемым
chmod +x /opt/trendpulse-ai/deploy.sh
```

## 4. Первоначальное развертывание

```bash
# Запускаем скрипт развертывания
/opt/trendpulse-ai/deploy.sh
```

## 5. Настройка автоматического развертывания (опционально)

### Создание GitHub Actions (если используете GitHub)

Создайте файл `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Server

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: 45.142.122.145
        username: root
        password: ${{ secrets.SERVER_PASSWORD }}
        script: |
          cd /opt/trendpulse-ai
          ./deploy.sh
```

### Настройка секретов в GitHub
1. Зайдите в настройки репозитория
2. Secrets and variables → Actions
3. Добавьте секрет `SERVER_PASSWORD` со значением `W5AV!54uq@5EMXLA`

## 6. Рабочий процесс разработки

### Локальная разработка
```bash
# Внесите изменения в код
git add .
git commit -m "Описание изменений"
git push origin main
```

### Автоматическое развертывание
После push в main:
- GitHub Actions автоматически развернет на сервере (если настроено)
- Или выполните вручную: `ssh root@45.142.122.145 "cd /opt/trendpulse-ai && ./deploy.sh"`

## 7. Полезные команды для управления

### Обновление на сервере
```bash
ssh root@45.142.122.145
cd /opt/trendpulse-ai
./deploy.sh
```

### Просмотр логов
```bash
ssh root@45.142.122.145
cd /opt/trendpulse-ai
docker-compose logs -f
```

### Перезапуск сервисов
```bash
ssh root@45.142.122.145
cd /opt/trendpulse-ai
docker-compose restart
```

### Проверка статуса
```bash
ssh root@45.142.122.145
cd /opt/trendpulse-ai
docker-compose ps
```

## 8. Структура репозитория

```
trendpulse-ai/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── services.py
│   ├── database.py
│   └── crud.py
├── bot/
│   ├── __init__.py
│   ├── main.py
│   └── handlers.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.bot
├── .env.example
├── .gitignore
├── README.md
└── deploy.sh
```

## 9. Безопасность

### Файл .env.example
Создайте файл `.env.example` с примером переменных окружения (без реальных токенов):

```bash
cat > .env.example << 'EOF'
# Telegram Bot Token
BOT_TOKEN=your_bot_token_here

# База данных
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/trendpulse

# Окружение
ENVIRONMENT=production

# API URL (для бота)
API_URL=http://backend:8000
EOF
```

### Добавление .env в .gitignore
Убедитесь, что `.env` добавлен в `.gitignore`, чтобы токены не попали в репозиторий.

## 10. Мониторинг и логирование

### Настройка логирования
```bash
# Создание директорий для логов
mkdir -p /opt/trendpulse-ai/logs
mkdir -p /opt/trendpulse-ai/reports
```

### Просмотр логов в реальном времени
```bash
ssh root@45.142.122.145
cd /opt/trendpulse-ai
docker-compose logs -f backend
docker-compose logs -f bot
```

Теперь у вас есть полноценная система развертывания через Git! 🚀 
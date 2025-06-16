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
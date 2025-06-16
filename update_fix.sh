#!/bin/bash

echo "🔄 Обновление TrendPulse AI с исправлением фильтрации проектов..."

# Остановка контейнеров
echo "⏹️ Останавливаем контейнеры..."
docker-compose down

# Пересборка образов
echo "🔨 Пересобираем образы..."
docker-compose build --no-cache

# Запуск контейнеров
echo "🚀 Запускаем контейнеры..."
docker-compose up -d

# Ожидание запуска
echo "⏳ Ждем запуска сервисов..."
sleep 10

# Проверка статуса
echo "🔍 Проверяем статус сервисов..."
docker-compose ps

# Проверка логов
echo "📋 Проверяем логи backend..."
docker-compose logs backend | tail -20

echo "📋 Проверяем логи бота..."
docker-compose logs bot | tail -20

echo "✅ Обновление завершено!"
echo ""
echo "🧪 Для тестирования выполните:"
echo "curl 'http://localhost:8000/projects/?user_id=307631283'"
echo ""
echo "📱 Теперь бот должен показывать только ваши проекты!" 
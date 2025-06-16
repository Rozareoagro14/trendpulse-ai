#!/bin/bash

echo "🔧 Исправление проблем с деплоем..."

# Останавливаем контейнеры
echo "🛑 Останавливаем контейнеры..."
docker compose down

# Решаем конфликт с Git
echo "📥 Решаем конфликт с Git..."
git stash
git pull origin main
git stash pop

# Пересобираем образы
echo "🔨 Пересобираем образы..."
docker compose build --no-cache

# Запускаем контейнеры
echo "▶️ Запускаем контейнеры..."
docker compose up -d

# Ждем запуска
echo "⏳ Ждем запуска сервисов..."
sleep 20

# Проверяем статус
echo "📊 Проверяем статус сервисов..."
docker compose ps

# Проверяем API
echo "🔍 Проверяем API..."
sleep 5
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API работает"
else
    echo "❌ API не отвечает"
    echo "📋 Проверяем логи backend..."
    docker compose logs backend --tail=20
fi

# Проверяем бота
echo "🤖 Проверяем бота..."
if docker compose ps | grep -q "bot.*running"; then
    echo "✅ Бот работает"
else
    echo "❌ Бот не работает"
    echo "📋 Проверяем логи бота..."
    docker compose logs bot --tail=10
fi

# Генерируем сценарии
echo "📈 Генерируем сценарии для всех проектов..."
if [ -f "generate_all_scenarios.py" ]; then
    python3 generate_all_scenarios.py
else
    echo "⚠️ Скрипт generate_all_scenarios.py не найден"
fi

echo "🎉 Исправление завершено!"
echo "📱 Бот: @TrendPulseAI_bot"
echo "🌐 API: http://localhost:8000"
echo "📊 Документация: http://localhost:8000/docs" 
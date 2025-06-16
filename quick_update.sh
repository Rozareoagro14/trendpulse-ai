#!/bin/bash

echo "🚀 Быстрое обновление TrendPulse AI..."

# Проверяем, что Docker запущен
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker не запущен. Запустите Docker и попробуйте снова."
    exit 1
fi

# Останавливаем контейнеры
echo "🛑 Останавливаем контейнеры..."
docker compose down

# Пересобираем только измененные образы
echo "🔨 Пересобираем измененные образы..."
docker compose build --no-cache

# Запускаем контейнеры
echo "▶️ Запускаем контейнеры..."
docker compose up -d

# Ждем запуска
echo "⏳ Ждем запуска сервисов..."
sleep 10

# Проверяем статус
echo "📊 Проверяем статус сервисов..."
docker compose ps

# Проверяем API
echo "🔍 Проверяем API..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API работает"
else
    echo "❌ API не отвечает"
fi

# Генерируем сценарии для всех проектов
echo "📈 Генерируем сценарии для всех проектов..."
python generate_all_scenarios.py

echo "🎉 Обновление завершено!"
echo "📱 Бот: @TrendPulseAI_bot"
echo "🌐 API: http://localhost:8000"
echo "📊 Документация: http://localhost:8000/docs" 
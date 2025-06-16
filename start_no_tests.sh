#!/bin/bash

echo "🚀 Запуск системы без тестов..."

# Останавливаем контейнеры
echo "🛑 Останавливаем контейнеры..."
docker compose down

# Запускаем только базу данных
echo "🗄️ Запускаем базу данных..."
docker compose up -d db

# Ждем готовности базы
echo "⏳ Ждем готовности базы данных..."
sleep 10

# Запускаем backend без тестов
echo "🔧 Запускаем backend без тестов..."
docker compose run -d --rm backend uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Ждем запуска backend
echo "⏳ Ждем запуска backend..."
sleep 20

# Проверяем API
echo "🔍 Проверяем API..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API работает"
    
    # Запускаем бота без тестов
    echo "🤖 Запускаем бота без тестов..."
    docker compose run -d --rm bot python3 bot/main.py
    
    # Ждем запуска бота
    echo "⏳ Ждем запуска бота..."
    sleep 10
    
    # Финальная проверка
    echo "📊 Финальная проверка..."
    docker compose ps
    
    echo "🎉 Система успешно запущена без тестов!"
    echo "📱 Бот: @TrendPulseAI_bot"
    echo "🌐 API: http://localhost:8000"
    echo "📊 Документация: http://localhost:8000/docs"
    
else
    echo "❌ API не работает"
    echo "📋 Логи backend:"
    docker compose logs backend --tail=20
fi 
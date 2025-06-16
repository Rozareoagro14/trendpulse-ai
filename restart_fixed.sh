#!/bin/bash

echo "🚀 Быстрый перезапуск с исправленными тестами..."

# Останавливаем контейнеры
echo "🛑 Останавливаем контейнеры..."
docker compose down

# Запускаем только базу данных
echo "🗄️ Запускаем базу данных..."
docker compose up -d db

# Ждем готовности базы
echo "⏳ Ждем готовности базы данных..."
sleep 10

# Запускаем backend с исправленными тестами
echo "🔧 Запускаем backend с исправленными тестами..."
docker compose up -d backend

# Ждем запуска backend
echo "⏳ Ждем запуска backend..."
sleep 25

# Проверяем API
echo "🔍 Проверяем API..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API работает"
    
    # Запускаем бота с упрощенными тестами
    echo "🤖 Запускаем бота с упрощенными тестами..."
    docker compose up -d bot
    
    # Ждем запуска бота
    echo "⏳ Ждем запуска бота..."
    sleep 15
    
    # Финальная проверка
    echo "📊 Финальная проверка..."
    docker compose ps
    
    echo "🎉 Система успешно запущена с исправленными тестами!"
    echo "📱 Бот: @TrendPulseAI_bot"
    echo "🌐 API: http://localhost:8000"
    echo "📊 Документация: http://localhost:8000/docs"
    
else
    echo "❌ API не работает"
    echo "📋 Логи backend:"
    docker compose logs backend --tail=20
fi 
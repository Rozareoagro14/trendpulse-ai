#!/bin/bash

echo "🚀 Запуск системы без тестов..."

# Останавливаем все контейнеры
echo "🛑 Останавливаем контейнеры..."
docker compose down
docker compose -f docker-compose.no-tests.yml down

# Запускаем систему без тестов
echo "🚀 Запускаем систему без тестов..."
docker compose -f docker-compose.no-tests.yml up -d

# Ждем запуска
echo "⏳ Ждем запуска системы..."
sleep 30

# Проверяем API
echo "🔍 Проверяем API..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API работает"
    
    # Финальная проверка
    echo "📊 Финальная проверка..."
    docker compose -f docker-compose.no-tests.yml ps
    
    echo "🎉 Система успешно запущена без тестов!"
    echo "📱 Бот: @TrendPulseAI_bot"
    echo "🌐 API: http://localhost:8000"
    echo "📊 Документация: http://localhost:8000/docs"
    
else
    echo "❌ API не работает"
    echo "📋 Логи backend:"
    docker compose -f docker-compose.no-tests.yml logs backend --tail=20
fi 
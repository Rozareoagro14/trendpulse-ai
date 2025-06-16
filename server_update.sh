#!/bin/bash

echo "🚀 Быстрое обновление TrendPulse AI на сервере..."

# Проверяем, что мы в правильной директории
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Файл docker-compose.yml не найден. Перейдите в директорию проекта."
    exit 1
fi

# Останавливаем контейнеры
echo "🛑 Останавливаем контейнеры..."
docker compose down

# Обновляем код из Git
echo "📥 Обновляем код из Git..."
git pull origin main

# Пересобираем образы с новой функциональностью
echo "🔨 Пересобираем образы с новыми возможностями..."
docker compose build --no-cache

# Запускаем контейнеры
echo "▶️ Запускаем обновленные контейнеры..."
docker compose up -d

# Ждем запуска сервисов
echo "⏳ Ждем запуска сервисов..."
sleep 15

# Проверяем статус
echo "📊 Проверяем статус сервисов..."
docker compose ps

# Проверяем API
echo "🔍 Проверяем API..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API работает"
else
    echo "❌ API не отвечает"
    echo "📋 Проверяем логи..."
    docker compose logs backend --tail=20
fi

# Генерируем сценарии для всех проектов
echo "📈 Генерируем сценарии для всех проектов..."
python3 generate_all_scenarios.py

# Финальная проверка
echo "🎯 Финальная проверка системы..."
echo "📱 Бот: @TrendPulseAI_bot"
echo "🌐 API: http://localhost:8000"
echo "📊 Документация: http://localhost:8000/docs"

echo "🎉 Обновление завершено!"
echo ""
echo "✨ Новые возможности:"
echo "  ✅ Автоматическая генерация сценариев при создании проекта"
echo "  ✅ Интерактивный просмотр сценариев с детальным анализом"
echo "  ✅ Возможность выбора и просмотра деталей каждого сценария"
echo "  ✅ Генерация альтернативных сценариев"
echo "  ✅ PDF отчеты по сценариям"
echo "  ✅ Быстрые обновления с volumes"
echo ""
echo "🚀 Система готова к использованию!" 
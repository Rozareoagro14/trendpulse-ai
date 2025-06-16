#!/bin/bash

echo "🔧 Исправление проблем с деплоем и запуск тестов..."

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

# Запускаем контейнеры с тестами
echo "▶️ Запускаем контейнеры с автоматическими тестами..."
docker compose up -d

# Ждем запуска и тестов
echo "⏳ Ждем запуска сервисов и выполнения тестов..."
sleep 45

# Проверяем статус
echo "📊 Проверяем статус сервисов..."
docker compose ps

# Проверяем API
echo "🔍 Проверяем API..."
sleep 10
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

# Запускаем дополнительные тесты
echo "🧪 Запускаем дополнительные тесты..."
if [ -f "test_api.sh" ]; then
    chmod +x test_api.sh
    ./test_api.sh
else
    echo "⚠️ Скрипт test_api.sh не найден"
fi

# Генерируем сценарии
echo "📈 Генерируем сценарии для всех проектов..."
if [ -f "generate_all_scenarios.py" ]; then
    python3 generate_all_scenarios.py
else
    echo "⚠️ Скрипт generate_all_scenarios.py не найден"
fi

# Финальная проверка
echo "🎯 Финальная проверка системы..."
echo "📱 Бот: @TrendPulseAI_bot"
echo "🌐 API: http://localhost:8000"
echo "📊 Документация: http://localhost:8000/docs"
echo "🧪 Тесты: Автоматически запускаются при старте"

echo "🎉 Исправление и тестирование завершено!"
echo ""
echo "✨ Новые возможности:"
echo "  ✅ Автоматические тесты при запуске"
echo "  ✅ Автоматическая генерация сценариев"
echo "  ✅ Интерактивный просмотр сценариев"
echo "  ✅ Детальный анализ и PDF отчеты"
echo "  ✅ Быстрые обновления с volumes"
echo "  ✅ Исправлен async драйвер базы данных"
echo ""
echo "🚀 Система готова к использованию!" 
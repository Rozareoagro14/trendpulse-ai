#!/bin/bash

echo "🔧 Исправление подрядчиков в базе данных..."

# Установка pip если его нет
if ! command -v pip3 &> /dev/null; then
    echo "📦 Устанавливаем pip3..."
    apt update && apt install -y python3-pip
fi

# Установка httpx
echo "📦 Устанавливаем httpx..."
pip3 install httpx

# Очистка дублированных подрядчиков (оставляем только первого)
echo "🧹 Очищаем дублированные подрядчики..."
docker-compose exec db psql -U trendpulse -d trendpulse_db -c "DELETE FROM contractors WHERE id > 1;"

# Добавление разнообразных подрядчиков
echo "➕ Добавляем разнообразных подрядчиков..."
python3 add_contractors.py

# Проверка результата
echo "📊 Проверяем результат..."
curl -s "http://localhost:8000/contractors/" | jq '.[] | {id, name, specialization, rating}'

echo "✅ Исправление завершено!"
echo "📱 Теперь в боте должны показываться разные подрядчики без дублирования!" 
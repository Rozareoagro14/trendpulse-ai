#!/bin/bash

echo "🔍 Проверка сценариев в базе данных..."

echo "📊 Проекты пользователя 307631283:"
docker-compose exec db psql -U trendpulse -d trendpulse_db -c "SELECT id, name FROM projects WHERE user_id = 307631283;"

echo ""
echo "📈 Сценарии для проекта 'Влад' (ID=21):"
docker-compose exec db psql -U trendpulse -d trendpulse_db -c "SELECT id, name, roi, estimated_cost FROM scenarios WHERE project_id = 21;"

echo ""
echo "📈 Сценарии для проекта 'Вован' (ID=22):"
docker-compose exec db psql -U trendpulse -d trendpulse_db -c "SELECT id, name, roi, estimated_cost FROM scenarios WHERE project_id = 22;"

echo ""
echo "📊 Все сценарии в базе:"
docker-compose exec db psql -U trendpulse -d trendpulse_db -c "SELECT id, project_id, name FROM scenarios;"

echo ""
echo "🧪 Проверка API сценариев:"
echo "Сценарии для проекта 21:"
curl -s "http://localhost:8000/projects/21/scenarios/" | jq .

echo ""
echo "Сценарии для проекта 22:"
curl -s "http://localhost:8000/projects/22/scenarios/" | jq . 
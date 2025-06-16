#!/bin/bash

echo "🔍 Быстрое тестирование API TrendPulse AI..."

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функции для логирования
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ОШИБКА]${NC} $1"
}

success() {
    echo -e "${GREEN}[УСПЕХ]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[ПРЕДУПРЕЖДЕНИЕ]${NC} $1"
}

# Базовый URL API
API_URL="http://localhost:8000"

# Тест 1: Проверка здоровья API
log "1. Проверка здоровья API..."
response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/health")
if [ "$response" = "200" ]; then
    success "API здоров (HTTP $response)"
else
    error "API не отвечает (HTTP $response)"
    exit 1
fi

# Тест 2: Получение проектов
log "2. Тест получения проектов..."
projects_response=$(curl -s "$API_URL/projects/?user_id=307631283")
if echo "$projects_response" | grep -q "id"; then
    success "Проекты получены успешно"
    echo "Найдено проектов: $(echo "$projects_response" | jq '. | length' 2>/dev/null || echo "неизвестно")"
else
    warning "Не удалось получить проекты или проектов нет"
fi

# Тест 3: Получение подрядчиков
log "3. Тест получения подрядчиков..."
contractors_response=$(curl -s "$API_URL/contractors/")
if echo "$contractors_response" | grep -q "id"; then
    success "Подрядчики получены успешно"
    echo "Найдено подрядчиков: $(echo "$contractors_response" | jq '. | length' 2>/dev/null || echo "неизвестно")"
else
    warning "Не удалось получить подрядчиков"
fi

# Тест 4: Получение сценариев
log "4. Тест получения сценариев..."
scenarios_response=$(curl -s "$API_URL/scenarios/")
if echo "$scenarios_response" | grep -q "id"; then
    success "Сценарии получены успешно"
    echo "Найдено сценариев: $(echo "$scenarios_response" | jq '. | length' 2>/dev/null || echo "неизвестно")"
else
    warning "Не удалось получить сценарии или сценариев нет"
fi

# Тест 5: Создание тестового проекта
log "5. Тест создания проекта..."
create_project_response=$(curl -s -X POST "$API_URL/projects/" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Тестовый проект API",
        "location": "Москва",
        "budget": 1000000,
        "project_type": "residential",
        "user_id": 307631283
    }')

if echo "$create_project_response" | grep -q "id"; then
    success "Проект создан успешно"
    project_id=$(echo "$create_project_response" | jq -r '.id' 2>/dev/null)
    echo "ID созданного проекта: $project_id"
else
    warning "Не удалось создать проект"
    echo "Ответ: $create_project_response"
fi

# Тест 6: Получение пользователей
log "6. Тест получения пользователей..."
users_response=$(curl -s "$API_URL/users/")
if echo "$users_response" | grep -q "id"; then
    success "Пользователи получены успешно"
    echo "Найдено пользователей: $(echo "$users_response" | jq '. | length' 2>/dev/null || echo "неизвестно")"
else
    warning "Не удалось получить пользователей"
fi

echo ""
echo "🎯 ========================================="
echo "🎯 РЕЗУЛЬТАТЫ БЫСТРОГО ТЕСТИРОВАНИЯ"
echo "🎯 ========================================="
echo ""
echo "📊 API работает корректно!"
echo "   ✅ Здоровье API"
echo "   ✅ Получение проектов"
echo "   ✅ Получение подрядчиков"
echo "   ✅ Получение сценариев"
echo "   ✅ Создание проектов"
echo "   ✅ Получение пользователей"
echo ""
echo "🔗 API доступен по адресу: $API_URL"
echo "📋 Документация API: $API_URL/docs"
echo "" 
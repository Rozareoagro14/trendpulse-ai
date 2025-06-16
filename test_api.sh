#!/bin/bash

# Скрипт для тестирования API TrendPulse AI
# Запускать на сервере где работает система

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# URL API
API_URL="http://localhost:8000"

echo -e "${BLUE}🚀 TrendPulse AI - Тестирование API${NC}"
echo -e "${BLUE}🔗 API URL: ${API_URL}${NC}"
echo ""

# Функция для проверки статуса
check_status() {
    if [ $1 -eq 200 ]; then
        echo -e "${GREEN}✅ Успешно (${1})${NC}"
    else
        echo -e "${RED}❌ Ошибка (${1})${NC}"
        echo -e "${YELLOW}Ответ: ${2}${NC}"
    fi
}

# Тест 1: Health Check
echo -e "${BLUE}📊 Тест 1: Health Check${NC}"
response=$(curl -s -w "%{http_code}" -o /tmp/health_response.json "${API_URL}/health")
status_code=$(echo $response | tail -c 4)
response_body=$(cat /tmp/health_response.json)
check_status $status_code "$response_body"

if [ $status_code -eq 200 ]; then
    echo -e "${GREEN}📋 Статус: $(echo $response_body | jq -r '.status')${NC}"
    echo -e "${GREEN}📋 Версия: $(echo $response_body | jq -r '.version')${NC}"
fi
echo ""

# Тест 2: API Info
echo -e "${BLUE}📊 Тест 2: API Info${NC}"
response=$(curl -s -w "%{http_code}" -o /tmp/api_info_response.json "${API_URL}/api-info")
status_code=$(echo $response | tail -c 4)
response_body=$(cat /tmp/api_info_response.json)
check_status $status_code "$response_body"

if [ $status_code -eq 200 ]; then
    echo -e "${GREEN}📋 Имя: $(echo $response_body | jq -r '.name')${NC}"
    echo -e "${GREEN}📋 Версия: $(echo $response_body | jq -r '.version')${NC}"
    echo -e "${GREEN}📋 Возможности: $(echo $response_body | jq '.capabilities | length') функций${NC}"
fi
echo ""

# Тест 3: Создание проекта
echo -e "${BLUE}📊 Тест 3: Создание проекта${NC}"
project_data='{
    "name": "Тестовый жилой комплекс",
    "project_type": "residential_complex",
    "location": "Москва, ул. Тестовая, 1",
    "budget": 100000000,
    "area": 5000,
    "user_id": 12345
}'

response=$(curl -s -w "%{http_code}" -o /tmp/create_project_response.json \
    -H "Content-Type: application/json" \
    -d "$project_data" \
    "${API_URL}/projects/")
status_code=$(echo $response | tail -c 4)
response_body=$(cat /tmp/create_project_response.json)
check_status $status_code "$response_body"

if [ $status_code -eq 200 ]; then
    project_id=$(echo $response_body | jq -r '.id')
    echo -e "${GREEN}📋 ID проекта: ${project_id}${NC}"
    echo -e "${GREEN}📋 Название: $(echo $response_body | jq -r '.name')${NC}"
    echo -e "${GREEN}📋 Тип: $(echo $response_body | jq -r '.project_type')${NC}"
    echo -e "${GREEN}📋 Бюджет: $(echo $response_body | jq -r '.budget')${NC}"
    
    # Сохраняем ID для следующих тестов
    echo $project_id > /tmp/test_project_id
else
    echo -e "${RED}❌ Не удалось создать проект для дальнейших тестов${NC}"
    exit 1
fi
echo ""

# Тест 4: Получение списка проектов
echo -e "${BLUE}📊 Тест 4: Получение списка проектов${NC}"
response=$(curl -s -w "%{http_code}" -o /tmp/projects_list_response.json "${API_URL}/projects/")
status_code=$(echo $response | tail -c 4)
response_body=$(cat /tmp/projects_list_response.json)
check_status $status_code "$response_body"

if [ $status_code -eq 200 ]; then
    projects_count=$(echo $response_body | jq '. | length')
    echo -e "${GREEN}📋 Найдено проектов: ${projects_count}${NC}"
    
    if [ $projects_count -gt 0 ]; then
        first_project=$(echo $response_body | jq '.[0]')
        echo -e "${GREEN}📋 Первый проект: $(echo $first_project | jq -r '.name')${NC}"
    fi
fi
echo ""

# Тест 5: Получение проекта по ID
if [ -f /tmp/test_project_id ]; then
    project_id=$(cat /tmp/test_project_id)
    echo -e "${BLUE}📊 Тест 5: Получение проекта по ID (${project_id})${NC}"
    
    response=$(curl -s -w "%{http_code}" -o /tmp/get_project_response.json "${API_URL}/projects/${project_id}")
    status_code=$(echo $response | tail -c 4)
    response_body=$(cat /tmp/get_project_response.json)
    check_status $status_code "$response_body"
    
    if [ $status_code -eq 200 ]; then
        echo -e "${GREEN}📋 Название: $(echo $response_body | jq -r '.name')${NC}"
        echo -e "${GREEN}📋 Локация: $(echo $response_body | jq -r '.location')${NC}"
    fi
    echo ""
fi

# Тест 6: Создание подрядчика
echo -e "${BLUE}📊 Тест 6: Создание подрядчика${NC}"
contractor_data='{
    "name": "ООО Тестовый Подрядчик",
    "specialization": "Жилое строительство",
    "rating": 4.5,
    "contact_phone": "+7 (999) 123-45-67",
    "contact_email": "test@contractor.ru",
    "experience_years": 10,
    "completed_projects": 25
}'

response=$(curl -s -w "%{http_code}" -o /tmp/create_contractor_response.json \
    -H "Content-Type: application/json" \
    -d "$contractor_data" \
    "${API_URL}/contractors/")
status_code=$(echo $response | tail -c 4)
response_body=$(cat /tmp/create_contractor_response.json)
check_status $status_code "$response_body"

if [ $status_code -eq 200 ]; then
    echo -e "${GREEN}📋 Название: $(echo $response_body | jq -r '.name')${NC}"
    echo -e "${GREEN}📋 Специализация: $(echo $response_body | jq -r '.specialization')${NC}"
    echo -e "${GREEN}📋 Рейтинг: $(echo $response_body | jq -r '.rating')${NC}"
fi
echo ""

# Тест 7: Получение списка подрядчиков
echo -e "${BLUE}📊 Тест 7: Получение списка подрядчиков${NC}"
response=$(curl -s -w "%{http_code}" -o /tmp/contractors_list_response.json "${API_URL}/contractors/")
status_code=$(echo $response | tail -c 4)
response_body=$(cat /tmp/contractors_list_response.json)
check_status $status_code "$response_body"

if [ $status_code -eq 200 ]; then
    contractors_count=$(echo $response_body | jq '. | length')
    echo -e "${GREEN}📋 Найдено подрядчиков: ${contractors_count}${NC}"
fi
echo ""

# Тест 8: Получение простых сценариев
echo -e "${BLUE}📊 Тест 8: Получение простых сценариев${NC}"
response=$(curl -s -w "%{http_code}" -o /tmp/scenarios_response.json "${API_URL}/scenarios")
status_code=$(echo $response | tail -c 4)
response_body=$(cat /tmp/scenarios_response.json)
check_status $status_code "$response_body"

if [ $status_code -eq 200 ]; then
    scenarios_count=$(echo $response_body | jq '. | length')
    echo -e "${GREEN}📋 Найдено сценариев: ${scenarios_count}${NC}"
    
    if [ $scenarios_count -gt 0 ]; then
        first_scenario=$(echo $response_body | jq '.[0]')
        echo -e "${GREEN}📋 Первый сценарий: $(echo $first_scenario | jq -r '.name')${NC}"
        echo -e "${GREEN}📋 ROI: $(echo $first_scenario | jq -r '.roi')%${NC}"
    fi
fi
echo ""

# Тест 9: Генерация сценариев для проекта
if [ -f /tmp/test_project_id ]; then
    project_id=$(cat /tmp/test_project_id)
    echo -e "${BLUE}📊 Тест 9: Генерация сценариев для проекта (${project_id})${NC}"
    
    response=$(curl -s -w "%{http_code}" -o /tmp/generate_scenarios_response.json \
        "${API_URL}/projects/${project_id}/scenarios/generate/?count=3")
    status_code=$(echo $response | tail -c 4)
    response_body=$(cat /tmp/generate_scenarios_response.json)
    check_status $status_code "$response_body"
    
    if [ $status_code -eq 200 ]; then
        scenarios_count=$(echo $response_body | jq '. | length')
        echo -e "${GREEN}📋 Сгенерировано сценариев: ${scenarios_count}${NC}"
        
        if [ $scenarios_count -gt 0 ]; then
            first_scenario=$(echo $response_body | jq '.[0]')
            echo -e "${GREEN}📋 Первый сценарий: $(echo $first_scenario | jq -r '.name')${NC}"
            echo -e "${GREEN}📋 ROI: $(echo $first_scenario | jq -r '.roi')%${NC}"
        fi
    fi
    echo ""
fi

# Тест 10: Статистика системы
echo -e "${BLUE}📊 Тест 10: Статистика системы${NC}"
response=$(curl -s -w "%{http_code}" -o /tmp/stats_response.json "${API_URL}/stats")
status_code=$(echo $response | tail -c 4)
response_body=$(cat /tmp/stats_response.json)
check_status $status_code "$response_body"

if [ $status_code -eq 200 ]; then
    echo -e "${GREEN}📋 Всего сценариев: $(echo $response_body | jq -r '.scenarios.total_scenarios')${NC}"
    echo -e "${GREEN}📋 Всего пользователей: $(echo $response_body | jq -r '.users.total_users')${NC}"
    echo -e "${GREEN}📋 Подрядчиков: $(echo $response_body | jq -r '.contractors_count')${NC}"
    echo -e "${GREEN}📋 Отчетов: $(echo $response_body | jq -r '.reports_generated')${NC}"
fi
echo ""

# Очистка временных файлов
rm -f /tmp/*_response.json /tmp/test_project_id

echo -e "${GREEN}🎉 Тестирование завершено!${NC}"
echo -e "${BLUE}📋 Результаты сохранены в логах выше${NC}" 
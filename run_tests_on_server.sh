#!/bin/bash

echo "🧪 Запуск тестов TrendPulse AI на сервере..."

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

# Проверяем, что мы в правильной директории
if [ ! -f "docker-compose.yml" ]; then
    error "Файл docker-compose.yml не найден. Убедитесь, что вы в директории /opt/trendpulse-ai"
    exit 1
fi

# Проверяем, что контейнеры запущены
log "1. Проверяем статус контейнеров..."
if ! docker-compose ps | grep -q "Up"; then
    error "Контейнеры не запущены. Запустите сначала docker-compose up -d"
    exit 1
fi
success "Контейнеры запущены"

# Проверяем API
log "2. Проверяем доступность API..."
for i in {1..5}; do
    response=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/health")
    if [ "$response" = "200" ]; then
        success "API доступен (HTTP $response)"
        break
    else
        warning "Попытка $i/5: API не отвечает (HTTP $response)"
        if [ $i -eq 5 ]; then
            error "API недоступен после 5 попыток"
            exit 1
        fi
        sleep 2
    fi
done

# Устанавливаем зависимости для тестов
log "3. Устанавливаем зависимости для тестов..."
if [ ! -d "tests" ]; then
    error "Директория tests не найдена"
    exit 1
fi

cd tests
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        success "Зависимости установлены"
    else
        warning "Ошибка при установке зависимостей, продолжаем..."
    fi
fi

# Запускаем тесты
log "4. Запускаем все тесты..."
echo ""

# Тест 1: Создание проектов
log "📊 Тест создания проектов..."
python -m pytest test_simple_project_creation.py -v
PROJECT_TEST_RESULT=$?

# Тест 2: API endpoints
log "🔗 Тест API endpoints..."
python -m pytest test_api_endpoints.py -v
API_TEST_RESULT=$?

# Тест 3: Подрядчики
log "👷 Тест подрядчиков..."
python -m pytest test_contractors.py -v
CONTRACTOR_TEST_RESULT=$?

# Тест 4: Сценарии
log "📈 Тест сценариев..."
python -m pytest test_scenarios.py -v
SCENARIO_TEST_RESULT=$?

# Тест 5: Общие тесты проектов
log "🏗️ Общие тесты проектов..."
python -m pytest test_projects.py -v
GENERAL_PROJECT_TEST_RESULT=$?

# Возвращаемся в корневую директорию
cd ..

# Подводим итоги
echo ""
echo "🎯 ========================================="
echo "🎯 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ"
echo "🎯 ========================================="
echo ""

if [ $PROJECT_TEST_RESULT -eq 0 ]; then
    success "✅ Тест создания проектов: ПРОЙДЕН"
else
    error "❌ Тест создания проектов: ПРОВАЛЕН"
fi

if [ $API_TEST_RESULT -eq 0 ]; then
    success "✅ Тест API endpoints: ПРОЙДЕН"
else
    error "❌ Тест API endpoints: ПРОВАЛЕН"
fi

if [ $CONTRACTOR_TEST_RESULT -eq 0 ]; then
    success "✅ Тест подрядчиков: ПРОЙДЕН"
else
    error "❌ Тест подрядчиков: ПРОВАЛЕН"
fi

if [ $SCENARIO_TEST_RESULT -eq 0 ]; then
    success "✅ Тест сценариев: ПРОЙДЕН"
else
    error "❌ Тест сценариев: ПРОВАЛЕН"
fi

if [ $GENERAL_PROJECT_TEST_RESULT -eq 0 ]; then
    success "✅ Общие тесты проектов: ПРОЙДЕН"
else
    error "❌ Общие тесты проектов: ПРОВАЛЕН"
fi

# Общий результат
TOTAL_FAILED=$((PROJECT_TEST_RESULT + API_TEST_RESULT + CONTRACTOR_TEST_RESULT + SCENARIO_TEST_RESULT + GENERAL_PROJECT_TEST_RESULT))

echo ""
if [ $TOTAL_FAILED -eq 0 ]; then
    echo "🎉 ========================================="
    echo "🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!"
    echo "🎉 ========================================="
    echo ""
    echo "📊 Система работает корректно:"
    echo "   ✅ Создание проектов"
    echo "   ✅ API endpoints"
    echo "   ✅ Подрядчики"
    echo "   ✅ Сценарии"
    echo "   ✅ Общая функциональность"
else
    echo "⚠️  ========================================="
    echo "⚠️  НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ"
    echo "⚠️  ========================================="
    echo ""
    echo "🔧 Рекомендации:"
    echo "   1. Проверьте логи контейнеров"
    echo "   2. Убедитесь, что база данных работает"
    echo "   3. Проверьте подключение к API"
    echo "   4. Запустите тесты повторно"
fi

echo ""
echo "📋 Полезные команды для диагностики:"
echo "   docker-compose logs backend    # Логи API"
echo "   docker-compose logs bot        # Логи бота"
echo "   curl localhost:8000/health     # Проверка API"
echo "   curl localhost:8000/projects/  # Проверка проектов"
echo "" 
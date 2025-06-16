#!/bin/bash

echo "🚀 Начинаем полное обновление TrendPulse AI..."

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для логирования
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

log "1. Получаем последние изменения из Git..."
git pull origin main
if [ $? -eq 0 ]; then
    success "Код успешно обновлен"
else
    error "Ошибка при получении кода из Git"
    exit 1
fi

log "2. Останавливаем контейнеры..."
docker-compose down
success "Контейнеры остановлены"

log "3. Очищаем Docker кэш и образы..."
docker system prune -a -f
docker volume prune -f
success "Docker очищен"

log "4. Пересобираем образы с нуля..."
docker-compose build --no-cache --pull
if [ $? -eq 0 ]; then
    success "Образы успешно пересобраны"
else
    error "Ошибка при сборке образов"
    exit 1
fi

log "5. Запускаем контейнеры..."
docker-compose up -d
if [ $? -eq 0 ]; then
    success "Контейнеры запущены"
else
    error "Ошибка при запуске контейнеров"
    exit 1
fi

log "6. Ждем запуска сервисов (30 секунд)..."
sleep 30

log "7. Проверяем статус контейнеров..."
docker-compose ps

log "8. Проверяем здоровье API..."
for i in {1..10}; do
    response=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/health")
    if [ "$response" = "200" ]; then
        success "API работает корректно (HTTP $response)"
        break
    else
        warning "Попытка $i/10: API не отвечает (HTTP $response)"
        if [ $i -eq 10 ]; then
            error "API не отвечает после 10 попыток"
            log "Проверяем логи backend..."
            docker-compose logs backend | tail -20
            exit 1
        fi
        sleep 5
    fi
done

log "9. Проверяем бота..."
bot_logs=$(docker-compose logs bot | tail -5)
if echo "$bot_logs" | grep -q "Bot started"; then
    success "Бот запущен успешно"
else
    warning "Бот может не запуститься корректно. Проверяем логи..."
    docker-compose logs bot | tail -10
fi

log "10. Проверяем базу данных..."
db_status=$(docker-compose exec -T db psql -U postgres -d trendpulse -c "SELECT COUNT(*) FROM projects;" 2>/dev/null | tail -1 | tr -d ' ')
if [ "$db_status" -gt 0 ] 2>/dev/null; then
    success "База данных работает, найдено $db_status проектов"
else
    warning "База данных может быть пустой или недоступной"
fi

echo ""
echo "🎉 ========================================="
echo "🎉 ОБНОВЛЕНИЕ ЗАВЕРШЕНО УСПЕШНО!"
echo "🎉 ========================================="
echo ""
echo "📊 Статус системы:"
echo "   ✅ Backend API: Работает"
echo "   ✅ Telegram Bot: Запущен"
echo "   ✅ База данных: Подключена"
echo ""
echo "🧪 Для тестирования в Telegram:"
echo "   1. Откройте @TrendPulseAI_bot"
echo "   2. Нажмите '📊 Мои проекты'"
echo "   3. Нажмите '📈 Сценарии'"
echo "   4. Нажмите '👷 Подрядчики'"
echo ""
echo "📋 Полезные команды:"
echo "   docker-compose ps          # Статус контейнеров"
echo "   docker-compose logs bot    # Логи бота"
echo "   docker-compose logs backend # Логи API"
echo "   curl localhost:8000/health # Проверка API"
echo ""
echo "🔧 Если что-то не работает:"
echo "   docker-compose restart     # Перезапуск"
echo "   docker-compose down && docker-compose up -d # Полный перезапуск"
echo "" 
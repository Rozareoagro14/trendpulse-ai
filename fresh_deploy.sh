#!/bin/bash

# 🚀 Скрипт полной переустановки TrendPulse AI
# Автор: TrendPulse AI Team
# Дата: $(date)

set -e  # Остановка при ошибке

echo "🚀 Начинаем полную переустановку TrendPulse AI..."

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для логирования
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
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

# Проверка, что мы в правильной директории
if [ ! -f ".env" ]; then
    error "Файл .env не найден. Убедитесь, что вы находитесь в директории проекта."
    exit 1
fi

log "📁 Текущая директория: $(pwd)"

# 1. Сохраняем .env файл
log "💾 Сохраняем .env файл..."
cp .env /tmp/trendpulse.env.backup
success ".env файл сохранен в /tmp/trendpulse.env.backup"

# 2. Останавливаем контейнеры
log "🛑 Останавливаем контейнеры..."
if [ -f "docker-compose.yml" ]; then
    docker-compose down || true
    success "Контейнеры остановлены"
else
    warning "docker-compose.yml не найден, пропускаем остановку контейнеров"
fi

# 3. Очищаем Docker
log "🧹 Очищаем Docker..."
docker container prune -f || true
docker image prune -a -f || true
docker volume prune -f || true
docker network prune -f || true
docker system prune -a -f || true
success "Docker очищен"

# 4. Удаляем старые файлы
log "🗑️ Удаляем старые файлы проекта..."
cd /opt
rm -rf trendpulse-ai
mkdir trendpulse-ai
cd trendpulse-ai
success "Старые файлы удалены, новая директория создана"

# 5. Восстанавливаем .env
log "📄 Восстанавливаем .env файл..."
cp /tmp/trendpulse.env.backup .env
success ".env файл восстановлен"

# 6. Скачиваем свежий код
log "📥 Скачиваем свежий код из репозитория..."
git clone https://github.com/Rozareoagro14/trendpulse-ai.git .
success "Код скачан из репозитория"

# 7. Проверяем структуру
log "📋 Проверяем структуру проекта..."
if [ ! -f "docker-compose.yml" ]; then
    error "docker-compose.yml не найден после клонирования"
    exit 1
fi

if [ ! -f "backend/main.py" ]; then
    error "backend/main.py не найден после клонирования"
    exit 1
fi

if [ ! -f "bot/main.py" ]; then
    error "bot/main.py не найден после клонирования"
    exit 1
fi

success "Структура проекта корректна"

# 8. Собираем образы
log "🔨 Собираем Docker образы..."
docker-compose build --no-cache
success "Образы собраны"

# 9. Запускаем контейнеры
log "🚀 Запускаем контейнеры..."
docker-compose up -d
success "Контейнеры запущены"

# 10. Ждем запуска
log "⏳ Ждем запуска контейнеров..."
sleep 10

# 11. Проверяем статус
log "📊 Проверяем статус контейнеров..."
docker-compose ps

# 12. Проверяем API
log "🔍 Проверяем API..."
for i in {1..30}; do
    if curl -s "http://localhost:8000/health" > /dev/null; then
        success "API отвечает на порту 8000"
        break
    fi
    if [ $i -eq 30 ]; then
        error "API не отвечает после 30 попыток"
        log "Проверяем логи..."
        docker-compose logs backend | tail -20
        exit 1
    fi
    sleep 2
done

# 13. Проверяем логи
log "📝 Проверяем логи..."
echo "=== Логи Backend ==="
docker-compose logs backend | tail -5
echo ""
echo "=== Логи Bot ==="
docker-compose logs bot | tail -5

# 14. Добавляем подрядчиков (если скрипт есть)
if [ -f "add_contractors.py" ]; then
    log "👷 Добавляем подрядчиков..."
    if command -v python3 &> /dev/null; then
        if command -v pip3 &> /dev/null; then
            pip3 install httpx || true
            python3 add_contractors.py || warning "Не удалось добавить подрядчиков"
        else
            warning "pip3 не установлен, пропускаем добавление подрядчиков"
        fi
    else
        warning "python3 не установлен, пропускаем добавление подрядчиков"
    fi
fi

# 15. Финальная проверка
log "✅ Финальная проверка..."
echo ""
echo "=== Статус контейнеров ==="
docker-compose ps
echo ""
echo "=== Проверка API ==="
curl -s "http://localhost:8000/health" | jq . 2>/dev/null || curl -s "http://localhost:8000/health"
echo ""
echo "=== Проверка проектов ==="
curl -s "http://localhost:8000/projects/" | jq '. | length' 2>/dev/null || echo "Не удалось проверить проекты"
echo ""
echo "=== Проверка подрядчиков ==="
curl -s "http://localhost:8000/contractors/" | jq '. | length' 2>/dev/null || echo "Не удалось проверить подрядчиков"

success "🎉 Переустановка завершена успешно!"
echo ""
echo "📱 Теперь можете проверить бота в Telegram:"
echo "   1. Откройте бота"
echo "   2. Нажмите '📊 Мои проекты'"
echo "   3. Нажмите '👷 Подрядчики'"
echo "   4. Нажмите '📈 Сценарии'"
echo ""
echo "🔧 Если что-то не работает, проверьте логи:"
echo "   docker-compose logs -f" 
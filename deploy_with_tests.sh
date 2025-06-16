#!/bin/bash

# Скрипт для деплоя TrendPulse AI с тестированием
# Запускать на сервере

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 TrendPulse AI - Деплой с тестированием${NC}"
echo ""

# Проверяем, что мы в правильной директории
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ Файл docker-compose.yml не найден. Перейдите в директорию проекта.${NC}"
    exit 1
fi

# 1. Получить последние изменения
echo -e "${BLUE}📥 Получение последних изменений из Git...${NC}"
git pull origin main
echo -e "${GREEN}✅ Код обновлен${NC}"
echo ""

# 2. Остановить контейнеры
echo -e "${BLUE}🛑 Остановка контейнеров...${NC}"
docker-compose down
echo -e "${GREEN}✅ Контейнеры остановлены${NC}"
echo ""

# 3. Пересобрать и запустить контейнеры
echo -e "${BLUE}🔨 Пересборка и запуск контейнеров...${NC}"
docker-compose up --build -d
echo -e "${GREEN}✅ Контейнеры запущены${NC}"
echo ""

# 4. Подождать инициализации
echo -e "${BLUE}⏳ Ожидание инициализации системы (60 секунд)...${NC}"
sleep 60
echo -e "${GREEN}✅ Система готова${NC}"
echo ""

# 5. Проверить статус контейнеров
echo -e "${BLUE}📊 Проверка статуса контейнеров...${NC}"
docker-compose ps
echo ""

# 6. Проверить логи backend
echo -e "${BLUE}📋 Логи backend (последние 10 строк):${NC}"
docker-compose logs backend | tail -10
echo ""

# 7. Проверить логи bot
echo -e "${BLUE}📋 Логи bot (последние 10 строк):${NC}"
docker-compose logs bot | tail -10
echo ""

# 8. Проверить API
echo -e "${BLUE}🔍 Проверка API...${NC}"
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ API доступен${NC}"
else
    echo -e "${RED}❌ API недоступен${NC}"
    exit 1
fi
echo ""

# 9. Запустить тесты
echo -e "${BLUE}🧪 Запуск тестов...${NC}"
if [ -f "test_api.sh" ]; then
    chmod +x test_api.sh
    ./test_api.sh
    echo -e "${GREEN}✅ Тесты завершены${NC}"
else
    echo -e "${YELLOW}⚠️ Файл test_api.sh не найден${NC}"
fi
echo ""

# 10. Финальная проверка
echo -e "${BLUE}🎯 Финальная проверка системы...${NC}"

# Проверяем API info
echo -e "${BLUE}📊 API Info:${NC}"
curl -s http://localhost:8000/api-info | jq -r '.name, .version' 2>/dev/null || echo "API info недоступен"

# Проверяем статистику
echo -e "${BLUE}📈 Статистика:${NC}"
curl -s http://localhost:8000/stats | jq -r '.scenarios.total_scenarios, .users.total_users, .contractors_count' 2>/dev/null || echo "Статистика недоступна"

echo ""
echo -e "${GREEN}🎉 Деплой завершен успешно!${NC}"
echo -e "${BLUE}📋 Система готова к работе${NC}"
echo -e "${BLUE}🔗 API: http://localhost:8000${NC}"
echo -e "${BLUE}🤖 Бот: @trendpulse_aiv2_bot${NC}"
echo ""

# 11. Показать команды для мониторинга
echo -e "${YELLOW}📋 Полезные команды для мониторинга:${NC}"
echo -e "${YELLOW}  docker-compose ps                    # Статус контейнеров${NC}"
echo -e "${YELLOW}  docker-compose logs -f backend       # Логи backend${NC}"
echo -e "${YELLOW}  docker-compose logs -f bot           # Логи bot${NC}"
echo -e "${YELLOW}  curl http://localhost:8000/health    # Проверка API${NC}"
echo -e "${YELLOW}  ./test_api.sh                        # Запуск тестов${NC}"
echo "" 
# Скрипт для деплоя TrendPulse AI с тестированием
# Запускать на сервере

param(
    [string]$ApiUrl = "http://localhost:8000"
)

# Цвета для вывода
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"

Write-Host "🚀 TrendPulse AI - Деплой с тестированием" -ForegroundColor $Blue
Write-Host ""

# Проверяем, что мы в правильной директории
if (-not (Test-Path "docker-compose.yml")) {
    Write-Host "❌ Файл docker-compose.yml не найден. Перейдите в директорию проекта." -ForegroundColor $Red
    exit 1
}

# 1. Получить последние изменения
Write-Host "📥 Получение последних изменений из Git..." -ForegroundColor $Blue
git pull origin main
Write-Host "✅ Код обновлен" -ForegroundColor $Green
Write-Host ""

# 2. Остановить контейнеры
Write-Host "🛑 Остановка контейнеров..." -ForegroundColor $Blue
docker-compose down
Write-Host "✅ Контейнеры остановлены" -ForegroundColor $Green
Write-Host ""

# 3. Пересобрать и запустить контейнеры
Write-Host "🔨 Пересборка и запуск контейнеров..." -ForegroundColor $Blue
docker-compose up --build -d
Write-Host "✅ Контейнеры запущены" -ForegroundColor $Green
Write-Host ""

# 4. Подождать инициализации
Write-Host "⏳ Ожидание инициализации системы (60 секунд)..." -ForegroundColor $Blue
Start-Sleep -Seconds 60
Write-Host "✅ Система готова" -ForegroundColor $Green
Write-Host ""

# 5. Проверить статус контейнеров
Write-Host "📊 Проверка статуса контейнеров..." -ForegroundColor $Blue
docker-compose ps
Write-Host ""

# 6. Проверить логи backend
Write-Host "📋 Логи backend (последние 10 строк):" -ForegroundColor $Blue
docker-compose logs backend | Select-Object -Last 10
Write-Host ""

# 7. Проверить логи bot
Write-Host "📋 Логи bot (последние 10 строк):" -ForegroundColor $Blue
docker-compose logs bot | Select-Object -Last 10
Write-Host ""

# 8. Проверить API
Write-Host "🔍 Проверка API..." -ForegroundColor $Blue
try {
    $response = Invoke-RestMethod -Uri "$ApiUrl/health" -Method Get -TimeoutSec 10
    Write-Host "✅ API доступен" -ForegroundColor $Green
} catch {
    Write-Host "❌ API недоступен" -ForegroundColor $Red
    exit 1
}
Write-Host ""

# 9. Запустить тесты
Write-Host "🧪 Запуск тестов..." -ForegroundColor $Blue
if (Test-Path "test_api.ps1") {
    & .\test_api.ps1 -ApiUrl $ApiUrl
    Write-Host "✅ Тесты завершены" -ForegroundColor $Green
} else {
    Write-Host "⚠️ Файл test_api.ps1 не найден" -ForegroundColor $Yellow
}
Write-Host ""

# 10. Финальная проверка
Write-Host "🎯 Финальная проверка системы..." -ForegroundColor $Blue

# Проверяем API info
Write-Host "📊 API Info:" -ForegroundColor $Blue
try {
    $apiInfo = Invoke-RestMethod -Uri "$ApiUrl/api-info" -Method Get
    Write-Host "  Имя: $($apiInfo.name)" -ForegroundColor $Green
    Write-Host "  Версия: $($apiInfo.version)" -ForegroundColor $Green
} catch {
    Write-Host "  API info недоступен" -ForegroundColor $Yellow
}

# Проверяем статистику
Write-Host "📈 Статистика:" -ForegroundColor $Blue
try {
    $stats = Invoke-RestMethod -Uri "$ApiUrl/stats" -Method Get
    Write-Host "  Сценариев: $($stats.scenarios.total_scenarios)" -ForegroundColor $Green
    Write-Host "  Пользователей: $($stats.users.total_users)" -ForegroundColor $Green
    Write-Host "  Подрядчиков: $($stats.contractors_count)" -ForegroundColor $Green
} catch {
    Write-Host "  Статистика недоступна" -ForegroundColor $Yellow
}

Write-Host ""
Write-Host "🎉 Деплой завершен успешно!" -ForegroundColor $Green
Write-Host "📋 Система готова к работе" -ForegroundColor $Blue
Write-Host "🔗 API: $ApiUrl" -ForegroundColor $Blue
Write-Host "🤖 Бот: @trendpulse_aiv2_bot" -ForegroundColor $Blue
Write-Host ""

# 11. Показать команды для мониторинга
Write-Host "📋 Полезные команды для мониторинга:" -ForegroundColor $Yellow
Write-Host "  docker-compose ps                    # Статус контейнеров" -ForegroundColor $Yellow
Write-Host "  docker-compose logs -f backend       # Логи backend" -ForegroundColor $Yellow
Write-Host "  docker-compose logs -f bot           # Логи bot" -ForegroundColor $Yellow
Write-Host "  curl $ApiUrl/health                  # Проверка API" -ForegroundColor $Yellow
Write-Host "  .\test_api.ps1                       # Запуск тестов" -ForegroundColor $Yellow
Write-Host "" 
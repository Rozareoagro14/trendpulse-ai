# PowerShell скрипт для обновления TrendPulse AI

Write-Host "🔄 Обновление TrendPulse AI с исправлением фильтрации проектов..." -ForegroundColor Green

# Остановка контейнеров
Write-Host "⏹️ Останавливаем контейнеры..." -ForegroundColor Yellow
docker-compose down

# Пересборка образов
Write-Host "🔨 Пересобираем образы..." -ForegroundColor Yellow
docker-compose build --no-cache

# Запуск контейнеров
Write-Host "🚀 Запускаем контейнеры..." -ForegroundColor Yellow
docker-compose up -d

# Ожидание запуска
Write-Host "⏳ Ждем запуска сервисов..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Проверка статуса
Write-Host "🔍 Проверяем статус сервисов..." -ForegroundColor Yellow
docker-compose ps

# Проверка логов
Write-Host "📋 Проверяем логи backend..." -ForegroundColor Yellow
docker-compose logs backend --tail=20

Write-Host "📋 Проверяем логи бота..." -ForegroundColor Yellow
docker-compose logs bot --tail=20

Write-Host "✅ Обновление завершено!" -ForegroundColor Green
Write-Host ""
Write-Host "🧪 Для тестирования выполните:" -ForegroundColor Cyan
Write-Host "curl 'http://localhost:8000/projects/?user_id=307631283'" -ForegroundColor White
Write-Host ""
Write-Host "📱 Теперь бот должен показывать только ваши проекты!" -ForegroundColor Green 
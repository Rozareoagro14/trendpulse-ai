# Быстрое исправление проблем с TrendPulse AI
Write-Host "🚀 Быстрое исправление проблем с TrendPulse AI..." -ForegroundColor Green

# Останавливаем контейнеры
Write-Host "🛑 Останавливаем контейнеры..." -ForegroundColor Yellow
docker compose down

# Очищаем образы
Write-Host "🧹 Очищаем старые образы..." -ForegroundColor Yellow
docker compose build --no-cache

# Запускаем только базу данных
Write-Host "🗄️ Запускаем базу данных..." -ForegroundColor Yellow
docker compose up -d db

# Ждем готовности базы
Write-Host "⏳ Ждем готовности базы данных..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Запускаем backend
Write-Host "🔧 Запускаем backend..." -ForegroundColor Yellow
docker compose up -d backend

# Ждем запуска backend
Write-Host "⏳ Ждем запуска backend..." -ForegroundColor Yellow
Start-Sleep -Seconds 20

# Проверяем API
Write-Host "🔍 Проверяем API..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ API работает" -ForegroundColor Green
        
        # Запускаем бота
        Write-Host "🤖 Запускаем бота..." -ForegroundColor Yellow
        docker compose up -d bot
        
        # Ждем запуска бота
        Write-Host "⏳ Ждем запуска бота..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
        
        # Финальная проверка
        Write-Host "📊 Финальная проверка..." -ForegroundColor Yellow
        docker compose ps
        
        Write-Host "🎉 Система успешно запущена!" -ForegroundColor Green
        Write-Host "📱 Бот: @TrendPulseAI_bot" -ForegroundColor Cyan
        Write-Host "🌐 API: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "📊 Документация: http://localhost:8000/docs" -ForegroundColor Cyan
        
    } else {
        Write-Host "❌ API не работает" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ API не работает" -ForegroundColor Red
    Write-Host "📋 Логи backend:" -ForegroundColor Yellow
    docker compose logs backend --tail=20
} 
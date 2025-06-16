# Быстрое обновление TrendPulse AI для Windows

Write-Host "🚀 Быстрое обновление TrendPulse AI..." -ForegroundColor Green

# Проверяем, что Docker запущен
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker не запущен. Запустите Docker и попробуйте снова." -ForegroundColor Red
    exit 1
}

# Останавливаем контейнеры
Write-Host "🛑 Останавливаем контейнеры..." -ForegroundColor Yellow
docker compose down

# Пересобираем только измененные образы
Write-Host "🔨 Пересобираем измененные образы..." -ForegroundColor Yellow
docker compose build --no-cache

# Запускаем контейнеры
Write-Host "▶️ Запускаем контейнеры..." -ForegroundColor Yellow
docker compose up -d

# Ждем запуска
Write-Host "⏳ Ждем запуска сервисов..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Проверяем статус
Write-Host "📊 Проверяем статус сервисов..." -ForegroundColor Yellow
docker compose ps

# Проверяем API
Write-Host "🔍 Проверяем API..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "✅ API работает" -ForegroundColor Green
} catch {
    Write-Host "❌ API не отвечает" -ForegroundColor Red
}

# Генерируем сценарии для всех проектов
Write-Host "📈 Генерируем сценарии для всех проектов..." -ForegroundColor Yellow
python generate_all_scenarios.py

Write-Host "🎉 Обновление завершено!" -ForegroundColor Green
Write-Host "📱 Бот: @TrendPulseAI_bot" -ForegroundColor Cyan
Write-Host "🌐 API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📊 Документация: http://localhost:8000/docs" -ForegroundColor Cyan 
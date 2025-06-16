# Быстрое обновление TrendPulse AI на сервере Windows

Write-Host "🚀 Быстрое обновление TrendPulse AI на сервере..." -ForegroundColor Green

# Проверяем, что мы в правильной директории
if (-not (Test-Path "docker-compose.yml")) {
    Write-Host "❌ Файл docker-compose.yml не найден. Перейдите в директорию проекта." -ForegroundColor Red
    exit 1
}

# Останавливаем контейнеры
Write-Host "🛑 Останавливаем контейнеры..." -ForegroundColor Yellow
docker compose down

# Обновляем код из Git
Write-Host "📥 Обновляем код из Git..." -ForegroundColor Yellow
git pull origin main

# Пересобираем образы с новой функциональностью
Write-Host "🔨 Пересобираем образы с новыми возможностями..." -ForegroundColor Yellow
docker compose build --no-cache

# Запускаем контейнеры
Write-Host "▶️ Запускаем обновленные контейнеры..." -ForegroundColor Yellow
docker compose up -d

# Ждем запуска сервисов
Write-Host "⏳ Ждем запуска сервисов..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

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
    Write-Host "📋 Проверяем логи..." -ForegroundColor Yellow
    docker compose logs backend --tail=20
}

# Генерируем сценарии для всех проектов
Write-Host "📈 Генерируем сценарии для всех проектов..." -ForegroundColor Yellow
python generate_all_scenarios.py

# Финальная проверка
Write-Host "🎯 Финальная проверка системы..." -ForegroundColor Green
Write-Host "📱 Бот: @TrendPulseAI_bot" -ForegroundColor Cyan
Write-Host "🌐 API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📊 Документация: http://localhost:8000/docs" -ForegroundColor Cyan

Write-Host "🎉 Обновление завершено!" -ForegroundColor Green
Write-Host "" -ForegroundColor White
Write-Host "✨ Новые возможности:" -ForegroundColor Yellow
Write-Host "  ✅ Автоматическая генерация сценариев при создании проекта" -ForegroundColor Green
Write-Host "  ✅ Интерактивный просмотр сценариев с детальным анализом" -ForegroundColor Green
Write-Host "  ✅ Возможность выбора и просмотра деталей каждого сценария" -ForegroundColor Green
Write-Host "  ✅ Генерация альтернативных сценариев" -ForegroundColor Green
Write-Host "  ✅ PDF отчеты по сценариям" -ForegroundColor Green
Write-Host "  ✅ Быстрые обновления с volumes" -ForegroundColor Green
Write-Host "" -ForegroundColor White
Write-Host "🚀 Система готова к использованию!" -ForegroundColor Green 
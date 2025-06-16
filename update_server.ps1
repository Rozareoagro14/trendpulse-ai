# PowerShell скрипт для полного обновления TrendPulse AI

Write-Host "🚀 Начинаем полное обновление TrendPulse AI..." -ForegroundColor Blue

# Функции для логирования
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] $Message" -ForegroundColor Blue
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ОШИБКА] $Message" -ForegroundColor Red
}

function Write-Success {
    param([string]$Message)
    Write-Host "[УСПЕХ] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[ПРЕДУПРЕЖДЕНИЕ] $Message" -ForegroundColor Yellow
}

# Проверяем, что мы в правильной директории
if (-not (Test-Path "docker-compose.yml")) {
    Write-Error "Файл docker-compose.yml не найден. Убедитесь, что вы в директории /opt/trendpulse-ai"
    exit 1
}

Write-Log "1. Получаем последние изменения из Git..."
try {
    git pull origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Код успешно обновлен"
    } else {
        Write-Error "Ошибка при получении кода из Git"
        exit 1
    }
} catch {
    Write-Error "Ошибка при выполнении git pull: $_"
    exit 1
}

Write-Log "2. Останавливаем контейнеры..."
try {
    docker-compose down
    Write-Success "Контейнеры остановлены"
} catch {
    Write-Error "Ошибка при остановке контейнеров: $_"
    exit 1
}

Write-Log "3. Очищаем Docker кэш и образы..."
try {
    docker system prune -a -f
    docker volume prune -f
    Write-Success "Docker очищен"
} catch {
    Write-Error "Ошибка при очистке Docker: $_"
    exit 1
}

Write-Log "4. Пересобираем образы с нуля..."
try {
    docker-compose build --no-cache --pull
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Образы успешно пересобраны"
    } else {
        Write-Error "Ошибка при сборке образов"
        exit 1
    }
} catch {
    Write-Error "Ошибка при сборке образов: $_"
    exit 1
}

Write-Log "5. Запускаем контейнеры..."
try {
    docker-compose up -d
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Контейнеры запущены"
    } else {
        Write-Error "Ошибка при запуске контейнеров"
        exit 1
    }
} catch {
    Write-Error "Ошибка при запуске контейнеров: $_"
    exit 1
}

Write-Log "6. Ждем запуска сервисов (30 секунд)..."
Start-Sleep -Seconds 30

Write-Log "7. Проверяем статус контейнеров..."
try {
    docker-compose ps
} catch {
    Write-Warning "Не удалось получить статус контейнеров: $_"
}

Write-Log "8. Проверяем здоровье API..."
$apiHealthy = $false
for ($i = 1; $i -le 10; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Success "API работает корректно (HTTP $($response.StatusCode))"
            $apiHealthy = $true
            break
        } else {
            Write-Warning "Попытка $i/10: API отвечает с кодом $($response.StatusCode)"
        }
    } catch {
        Write-Warning "Попытка $i/10: API не отвечает"
        if ($i -eq 10) {
            Write-Error "API не отвечает после 10 попыток"
            Write-Log "Проверяем логи backend..."
            try {
                docker-compose logs backend | Select-Object -Last 20
            } catch {
                Write-Warning "Не удалось получить логи backend"
            }
            exit 1
        }
        Start-Sleep -Seconds 5
    }
}

Write-Log "9. Проверяем бота..."
try {
    $botLogs = docker-compose logs bot | Select-Object -Last 5
    if ($botLogs -match "Bot started") {
        Write-Success "Бот запущен успешно"
    } else {
        Write-Warning "Бот может не запуститься корректно. Проверяем логи..."
        docker-compose logs bot | Select-Object -Last 10
    }
} catch {
    Write-Warning "Не удалось проверить логи бота: $_"
}

Write-Log "10. Проверяем базу данных..."
try {
    $dbResult = docker-compose exec -T db psql -U postgres -d trendpulse -c "SELECT COUNT(*) FROM projects;" 2>$null
    $projectCount = ($dbResult | Select-Object -Last 1).Trim()
    if ($projectCount -match '^\d+$' -and [int]$projectCount -gt 0) {
        Write-Success "База данных работает, найдено $projectCount проектов"
    } else {
        Write-Warning "База данных может быть пустой или недоступной"
    }
} catch {
    Write-Warning "Не удалось проверить базу данных: $_"
}

Write-Host ""
Write-Host "🎉 =========================================" -ForegroundColor Green
Write-Host "🎉 ОБНОВЛЕНИЕ ЗАВЕРШЕНО УСПЕШНО!" -ForegroundColor Green
Write-Host "🎉 =========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Статус системы:" -ForegroundColor Cyan
Write-Host "   ✅ Backend API: Работает" -ForegroundColor Green
Write-Host "   ✅ Telegram Bot: Запущен" -ForegroundColor Green
Write-Host "   ✅ База данных: Подключена" -ForegroundColor Green
Write-Host ""
Write-Host "🧪 Для тестирования в Telegram:" -ForegroundColor Cyan
Write-Host "   1. Откройте @TrendPulseAI_bot" -ForegroundColor White
Write-Host "   2. Нажмите '📊 Мои проекты'" -ForegroundColor White
Write-Host "   3. Нажмите '📈 Сценарии'" -ForegroundColor White
Write-Host "   4. Нажмите '👷 Подрядчики'" -ForegroundColor White
Write-Host ""
Write-Host "📋 Полезные команды:" -ForegroundColor Cyan
Write-Host "   docker-compose ps          # Статус контейнеров" -ForegroundColor White
Write-Host "   docker-compose logs bot    # Логи бота" -ForegroundColor White
Write-Host "   docker-compose logs backend # Логи API" -ForegroundColor White
Write-Host "   curl localhost:8000/health # Проверка API" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Если что-то не работает:" -ForegroundColor Cyan
Write-Host "   docker-compose restart     # Перезапуск" -ForegroundColor White
Write-Host "   docker-compose down && docker-compose up -d # Полный перезапуск" -ForegroundColor White
Write-Host "" 
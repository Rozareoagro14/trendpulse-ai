# PowerShell скрипт для запуска тестов TrendPulse AI на сервере

Write-Host "🧪 Запуск тестов TrendPulse AI на сервере..." -ForegroundColor Blue

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

# Проверяем, что контейнеры запущены
Write-Log "1. Проверяем статус контейнеров..."
try {
    $containerStatus = docker-compose ps
    if ($containerStatus -match "Up") {
        Write-Success "Контейнеры запущены"
    } else {
        Write-Error "Контейнеры не запущены. Запустите сначала docker-compose up -d"
        exit 1
    }
} catch {
    Write-Error "Ошибка при проверке статуса контейнеров: $_"
    exit 1
}

# Проверяем API
Write-Log "2. Проверяем доступность API..."
$apiAvailable = $false
for ($i = 1; $i -le 5; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Success "API доступен (HTTP $($response.StatusCode))"
            $apiAvailable = $true
            break
        } else {
            Write-Warning "Попытка $i/5: API отвечает с кодом $($response.StatusCode)"
        }
    } catch {
        Write-Warning "Попытка $i/5: API не отвечает"
        if ($i -eq 5) {
            Write-Error "API недоступен после 5 попыток"
            exit 1
        }
        Start-Sleep -Seconds 2
    }
}

# Устанавливаем зависимости для тестов
Write-Log "3. Устанавливаем зависимости для тестов..."
if (-not (Test-Path "tests")) {
    Write-Error "Директория tests не найдена"
    exit 1
}

Push-Location tests
if (Test-Path "requirements.txt") {
    try {
        pip install -r requirements.txt
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Зависимости установлены"
        } else {
            Write-Warning "Ошибка при установке зависимостей, продолжаем..."
        }
    } catch {
        Write-Warning "Ошибка при установке зависимостей: $_"
    }
}

# Запускаем тесты
Write-Log "4. Запускаем все тесты..."
Write-Host ""

# Тест 1: Создание проектов
Write-Log "📊 Тест создания проектов..."
try {
    python -m pytest test_simple_project_creation.py -v
    $PROJECT_TEST_RESULT = $LASTEXITCODE
} catch {
    Write-Error "Ошибка при запуске теста создания проектов: $_"
    $PROJECT_TEST_RESULT = 1
}

# Тест 2: API endpoints
Write-Log "🔗 Тест API endpoints..."
try {
    python -m pytest test_api_endpoints.py -v
    $API_TEST_RESULT = $LASTEXITCODE
} catch {
    Write-Error "Ошибка при запуске теста API endpoints: $_"
    $API_TEST_RESULT = 1
}

# Тест 3: Подрядчики
Write-Log "👷 Тест подрядчиков..."
try {
    python -m pytest test_contractors.py -v
    $CONTRACTOR_TEST_RESULT = $LASTEXITCODE
} catch {
    Write-Error "Ошибка при запуске теста подрядчиков: $_"
    $CONTRACTOR_TEST_RESULT = 1
}

# Тест 4: Сценарии
Write-Log "📈 Тест сценариев..."
try {
    python -m pytest test_scenarios.py -v
    $SCENARIO_TEST_RESULT = $LASTEXITCODE
} catch {
    Write-Error "Ошибка при запуске теста сценариев: $_"
    $SCENARIO_TEST_RESULT = 1
}

# Тест 5: Общие тесты проектов
Write-Log "🏗️ Общие тесты проектов..."
try {
    python -m pytest test_projects.py -v
    $GENERAL_PROJECT_TEST_RESULT = $LASTEXITCODE
} catch {
    Write-Error "Ошибка при запуске общих тестов проектов: $_"
    $GENERAL_PROJECT_TEST_RESULT = 1
}

# Возвращаемся в корневую директорию
Pop-Location

# Подводим итоги
Write-Host ""
Write-Host "🎯 =========================================" -ForegroundColor Cyan
Write-Host "🎯 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ" -ForegroundColor Cyan
Write-Host "🎯 =========================================" -ForegroundColor Cyan
Write-Host ""

if ($PROJECT_TEST_RESULT -eq 0) {
    Write-Success "✅ Тест создания проектов: ПРОЙДЕН"
} else {
    Write-Error "❌ Тест создания проектов: ПРОВАЛЕН"
}

if ($API_TEST_RESULT -eq 0) {
    Write-Success "✅ Тест API endpoints: ПРОЙДЕН"
} else {
    Write-Error "❌ Тест API endpoints: ПРОВАЛЕН"
}

if ($CONTRACTOR_TEST_RESULT -eq 0) {
    Write-Success "✅ Тест подрядчиков: ПРОЙДЕН"
} else {
    Write-Error "❌ Тест подрядчиков: ПРОВАЛЕН"
}

if ($SCENARIO_TEST_RESULT -eq 0) {
    Write-Success "✅ Тест сценариев: ПРОЙДЕН"
} else {
    Write-Error "❌ Тест сценариев: ПРОВАЛЕН"
}

if ($GENERAL_PROJECT_TEST_RESULT -eq 0) {
    Write-Success "✅ Общие тесты проектов: ПРОЙДЕН"
} else {
    Write-Error "❌ Общие тесты проектов: ПРОВАЛЕН"
}

# Общий результат
$TOTAL_FAILED = $PROJECT_TEST_RESULT + $API_TEST_RESULT + $CONTRACTOR_TEST_RESULT + $SCENARIO_TEST_RESULT + $GENERAL_PROJECT_TEST_RESULT

Write-Host ""
if ($TOTAL_FAILED -eq 0) {
    Write-Host "🎉 =========================================" -ForegroundColor Green
    Write-Host "🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!" -ForegroundColor Green
    Write-Host "🎉 =========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Система работает корректно:" -ForegroundColor Cyan
    Write-Host "   ✅ Создание проектов" -ForegroundColor Green
    Write-Host "   ✅ API endpoints" -ForegroundColor Green
    Write-Host "   ✅ Подрядчики" -ForegroundColor Green
    Write-Host "   ✅ Сценарии" -ForegroundColor Green
    Write-Host "   ✅ Общая функциональность" -ForegroundColor Green
} else {
    Write-Host "⚠️  =========================================" -ForegroundColor Yellow
    Write-Host "⚠️  НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ" -ForegroundColor Yellow
    Write-Host "⚠️  =========================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🔧 Рекомендации:" -ForegroundColor Cyan
    Write-Host "   1. Проверьте логи контейнеров" -ForegroundColor White
    Write-Host "   2. Убедитесь, что база данных работает" -ForegroundColor White
    Write-Host "   3. Проверьте подключение к API" -ForegroundColor White
    Write-Host "   4. Запустите тесты повторно" -ForegroundColor White
}

Write-Host ""
Write-Host "📋 Полезные команды для диагностики:" -ForegroundColor Cyan
Write-Host "   docker-compose logs backend    # Логи API" -ForegroundColor White
Write-Host "   docker-compose logs bot        # Логи бота" -ForegroundColor White
Write-Host "   curl localhost:8000/health     # Проверка API" -ForegroundColor White
Write-Host "   curl localhost:8000/projects/  # Проверка проектов" -ForegroundColor White
Write-Host "" 
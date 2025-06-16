# 🚀 Скрипт полной переустановки TrendPulse AI (PowerShell)
# Автор: TrendPulse AI Team
# Дата: $(Get-Date)

param(
    [switch]$Force
)

# Функция для логирования
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch ($Level) {
        "ERROR" { "Red" }
        "SUCCESS" { "Green" }
        "WARNING" { "Yellow" }
        default { "Blue" }
    }
    
    Write-Host "[$timestamp] $Message" -ForegroundColor $color
}

function Write-Error {
    param([string]$Message)
    Write-Log $Message "ERROR"
}

function Write-Success {
    param([string]$Message)
    Write-Log $Message "SUCCESS"
}

function Write-Warning {
    param([string]$Message)
    Write-Log $Message "WARNING"
}

Write-Host "🚀 Начинаем полную переустановку TrendPulse AI..." -ForegroundColor Cyan

# Проверка, что мы в правильной директории
if (-not (Test-Path ".env")) {
    Write-Error "Файл .env не найден. Убедитесь, что вы находитесь в директории проекта."
    exit 1
}

Write-Log "📁 Текущая директория: $(Get-Location)"

# 1. Сохраняем .env файл
Write-Log "💾 Сохраняем .env файл..."
Copy-Item ".env" "/tmp/trendpulse.env.backup" -Force
Write-Success ".env файл сохранен в /tmp/trendpulse.env.backup"

# 2. Останавливаем контейнеры
Write-Log "🛑 Останавливаем контейнеры..."
if (Test-Path "docker-compose.yml") {
    try {
        docker-compose down
        Write-Success "Контейнеры остановлены"
    }
    catch {
        Write-Warning "Не удалось остановить контейнеры: $_"
    }
}
else {
    Write-Warning "docker-compose.yml не найден, пропускаем остановку контейнеров"
}

# 3. Очищаем Docker
Write-Log "🧹 Очищаем Docker..."
try {
    docker container prune -f | Out-Null
    docker image prune -a -f | Out-Null
    docker volume prune -f | Out-Null
    docker network prune -f | Out-Null
    docker system prune -a -f | Out-Null
    Write-Success "Docker очищен"
}
catch {
    Write-Warning "Не удалось полностью очистить Docker: $_"
}

# 4. Удаляем старые файлы
Write-Log "🗑️ Удаляем старые файлы проекта..."
Set-Location "/opt"
if (Test-Path "trendpulse-ai") {
    Remove-Item "trendpulse-ai" -Recurse -Force
}
New-Item -ItemType Directory -Name "trendpulse-ai" | Out-Null
Set-Location "trendpulse-ai"
Write-Success "Старые файлы удалены, новая директория создана"

# 5. Восстанавливаем .env
Write-Log "📄 Восстанавливаем .env файл..."
Copy-Item "/tmp/trendpulse.env.backup" ".env" -Force
Write-Success ".env файл восстановлен"

# 6. Скачиваем свежий код
Write-Log "📥 Скачиваем свежий код из репозитория..."
try {
    git clone https://github.com/Rozareoagro14/trendpulse-ai.git .
    Write-Success "Код скачан из репозитория"
}
catch {
    Write-Error "Не удалось скачать код: $_"
    exit 1
}

# 7. Проверяем структуру
Write-Log "📋 Проверяем структуру проекта..."
if (-not (Test-Path "docker-compose.yml")) {
    Write-Error "docker-compose.yml не найден после клонирования"
    exit 1
}

if (-not (Test-Path "backend/main.py")) {
    Write-Error "backend/main.py не найден после клонирования"
    exit 1
}

if (-not (Test-Path "bot/main.py")) {
    Write-Error "bot/main.py не найден после клонирования"
    exit 1
}

Write-Success "Структура проекта корректна"

# 8. Собираем образы
Write-Log "🔨 Собираем Docker образы..."
try {
    docker-compose build --no-cache
    Write-Success "Образы собраны"
}
catch {
    Write-Error "Не удалось собрать образы: $_"
    exit 1
}

# 9. Запускаем контейнеры
Write-Log "🚀 Запускаем контейнеры..."
try {
    docker-compose up -d
    Write-Success "Контейнеры запущены"
}
catch {
    Write-Error "Не удалось запустить контейнеры: $_"
    exit 1
}

# 10. Ждем запуска
Write-Log "⏳ Ждем запуска контейнеров..."
Start-Sleep -Seconds 10

# 11. Проверяем статус
Write-Log "📊 Проверяем статус контейнеров..."
docker-compose ps

# 12. Проверяем API
Write-Log "🔍 Проверяем API..."
$apiReady = $false
for ($i = 1; $i -le 30; $i++) {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 5
        Write-Success "API отвечает на порту 8000"
        $apiReady = $true
        break
    }
    catch {
        if ($i -eq 30) {
            Write-Error "API не отвечает после 30 попыток"
            Write-Log "Проверяем логи..."
            docker-compose logs backend | Select-Object -Last 20
            exit 1
        }
        Start-Sleep -Seconds 2
    }
}

# 13. Проверяем логи
Write-Log "📝 Проверяем логи..."
Write-Host "=== Логи Backend ===" -ForegroundColor Yellow
docker-compose logs backend | Select-Object -Last 5
Write-Host ""
Write-Host "=== Логи Bot ===" -ForegroundColor Yellow
docker-compose logs bot | Select-Object -Last 5

# 14. Добавляем подрядчиков (если скрипт есть)
if (Test-Path "add_contractors.py") {
    Write-Log "👷 Добавляем подрядчиков..."
    try {
        if (Get-Command python3 -ErrorAction SilentlyContinue) {
            if (Get-Command pip3 -ErrorAction SilentlyContinue) {
                pip3 install httpx
                python3 add_contractors.py
                Write-Success "Подрядчики добавлены"
            }
            else {
                Write-Warning "pip3 не установлен, пропускаем добавление подрядчиков"
            }
        }
        else {
            Write-Warning "python3 не установлен, пропускаем добавление подрядчиков"
        }
    }
    catch {
        Write-Warning "Не удалось добавить подрядчиков: $_"
    }
}

# 15. Финальная проверка
Write-Log "✅ Финальная проверка..."
Write-Host ""
Write-Host "=== Статус контейнеров ===" -ForegroundColor Yellow
docker-compose ps
Write-Host ""
Write-Host "=== Проверка API ===" -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    $health | ConvertTo-Json
}
catch {
    Write-Warning "Не удалось проверить API: $_"
}
Write-Host ""
Write-Host "=== Проверка проектов ===" -ForegroundColor Yellow
try {
    $projects = Invoke-RestMethod -Uri "http://localhost:8000/projects/" -Method Get
    Write-Host "Количество проектов: $($projects.Count)"
}
catch {
    Write-Warning "Не удалось проверить проекты: $_"
}
Write-Host ""
Write-Host "=== Проверка подрядчиков ===" -ForegroundColor Yellow
try {
    $contractors = Invoke-RestMethod -Uri "http://localhost:8000/contractors/" -Method Get
    Write-Host "Количество подрядчиков: $($contractors.Count)"
}
catch {
    Write-Warning "Не удалось проверить подрядчиков: $_"
}

Write-Success "🎉 Переустановка завершена успешно!"
Write-Host ""
Write-Host "📱 Теперь можете проверить бота в Telegram:" -ForegroundColor Green
Write-Host "   1. Откройте бота" -ForegroundColor White
Write-Host "   2. Нажмите '📊 Мои проекты'" -ForegroundColor White
Write-Host "   3. Нажмите '👷 Подрядчики'" -ForegroundColor White
Write-Host "   4. Нажмите '📈 Сценарии'" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Если что-то не работает, проверьте логи:" -ForegroundColor Green
Write-Host "   docker-compose logs -f" -ForegroundColor White 
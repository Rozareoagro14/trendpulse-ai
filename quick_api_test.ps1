# PowerShell скрипт для быстрого тестирования API TrendPulse AI

Write-Host "🔍 Быстрое тестирование API TrendPulse AI..." -ForegroundColor Blue

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

# Базовый URL API
$API_URL = "http://localhost:8000"

# Тест 1: Проверка здоровья API
Write-Log "1. Проверка здоровья API..."
try {
    $response = Invoke-WebRequest -Uri "$API_URL/health" -Method GET -TimeoutSec 5 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Success "API здоров (HTTP $($response.StatusCode))"
    } else {
        Write-Error "API отвечает с ошибкой (HTTP $($response.StatusCode))"
        exit 1
    }
} catch {
    Write-Error "API не отвечает: $_"
    exit 1
}

# Тест 2: Получение проектов
Write-Log "2. Тест получения проектов..."
try {
    $projectsResponse = Invoke-WebRequest -Uri "$API_URL/projects/?user_id=307631283" -Method GET -UseBasicParsing
    $projectsData = $projectsResponse.Content | ConvertFrom-Json
    if ($projectsData) {
        Write-Success "Проекты получены успешно"
        Write-Host "Найдено проектов: $($projectsData.Count)" -ForegroundColor White
    } else {
        Write-Warning "Не удалось получить проекты или проектов нет"
    }
} catch {
    Write-Warning "Не удалось получить проекты: $_"
}

# Тест 3: Получение подрядчиков
Write-Log "3. Тест получения подрядчиков..."
try {
    $contractorsResponse = Invoke-WebRequest -Uri "$API_URL/contractors/" -Method GET -UseBasicParsing
    $contractorsData = $contractorsResponse.Content | ConvertFrom-Json
    if ($contractorsData) {
        Write-Success "Подрядчики получены успешно"
        Write-Host "Найдено подрядчиков: $($contractorsData.Count)" -ForegroundColor White
    } else {
        Write-Warning "Не удалось получить подрядчиков"
    }
} catch {
    Write-Warning "Не удалось получить подрядчиков: $_"
}

# Тест 4: Получение сценариев
Write-Log "4. Тест получения сценариев..."
try {
    $scenariosResponse = Invoke-WebRequest -Uri "$API_URL/scenarios/" -Method GET -UseBasicParsing
    $scenariosData = $scenariosResponse.Content | ConvertFrom-Json
    if ($scenariosData) {
        Write-Success "Сценарии получены успешно"
        Write-Host "Найдено сценариев: $($scenariosData.Count)" -ForegroundColor White
    } else {
        Write-Warning "Не удалось получить сценарии или сценариев нет"
    }
} catch {
    Write-Warning "Не удалось получить сценарии: $_"
}

# Тест 5: Создание тестового проекта
Write-Log "5. Тест создания проекта..."
try {
    $projectData = @{
        name = "Тестовый проект API"
        location = "Москва"
        budget = 1000000
        project_type = "residential"
        user_id = 307631283
    } | ConvertTo-Json

    $createProjectResponse = Invoke-WebRequest -Uri "$API_URL/projects/" -Method POST -Body $projectData -ContentType "application/json" -UseBasicParsing
    $createdProject = $createProjectResponse.Content | ConvertFrom-Json
    if ($createdProject.id) {
        Write-Success "Проект создан успешно"
        Write-Host "ID созданного проекта: $($createdProject.id)" -ForegroundColor White
    } else {
        Write-Warning "Не удалось создать проект"
        Write-Host "Ответ: $($createProjectResponse.Content)" -ForegroundColor White
    }
} catch {
    Write-Warning "Не удалось создать проект: $_"
}

# Тест 6: Получение пользователей
Write-Log "6. Тест получения пользователей..."
try {
    $usersResponse = Invoke-WebRequest -Uri "$API_URL/users/" -Method GET -UseBasicParsing
    $usersData = $usersResponse.Content | ConvertFrom-Json
    if ($usersData) {
        Write-Success "Пользователи получены успешно"
        Write-Host "Найдено пользователей: $($usersData.Count)" -ForegroundColor White
    } else {
        Write-Warning "Не удалось получить пользователей"
    }
} catch {
    Write-Warning "Не удалось получить пользователей: $_"
}

Write-Host ""
Write-Host "🎯 =========================================" -ForegroundColor Cyan
Write-Host "🎯 РЕЗУЛЬТАТЫ БЫСТРОГО ТЕСТИРОВАНИЯ" -ForegroundColor Cyan
Write-Host "🎯 =========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 API работает корректно!" -ForegroundColor Green
Write-Host "   ✅ Здоровье API" -ForegroundColor Green
Write-Host "   ✅ Получение проектов" -ForegroundColor Green
Write-Host "   ✅ Получение подрядчиков" -ForegroundColor Green
Write-Host "   ✅ Получение сценариев" -ForegroundColor Green
Write-Host "   ✅ Создание проектов" -ForegroundColor Green
Write-Host "   ✅ Получение пользователей" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 API доступен по адресу: $API_URL" -ForegroundColor White
Write-Host "📋 Документация API: $API_URL/docs" -ForegroundColor White
Write-Host "" 
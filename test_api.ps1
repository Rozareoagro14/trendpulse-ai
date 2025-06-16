# Скрипт для тестирования API TrendPulse AI
# Запускать на сервере где работает система

param(
    [string]$ApiUrl = "http://localhost:8000"
)

# Цвета для вывода
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"

Write-Host "🚀 TrendPulse AI - Тестирование API" -ForegroundColor $Blue
Write-Host "🔗 API URL: $ApiUrl" -ForegroundColor $Blue
Write-Host ""

# Функция для проверки статуса
function Check-Status {
    param($StatusCode, $ResponseBody)
    
    if ($StatusCode -eq 200) {
        Write-Host "✅ Успешно ($StatusCode)" -ForegroundColor $Green
    } else {
        Write-Host "❌ Ошибка ($StatusCode)" -ForegroundColor $Red
        Write-Host "Ответ: $ResponseBody" -ForegroundColor $Yellow
    }
}

# Тест 1: Health Check
Write-Host "📊 Тест 1: Health Check" -ForegroundColor $Blue
try {
    $response = Invoke-RestMethod -Uri "$ApiUrl/health" -Method Get
    Check-Status 200 $response
    
    Write-Host "📋 Статус: $($response.status)" -ForegroundColor $Green
    Write-Host "📋 Версия: $($response.version)" -ForegroundColor $Green
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Check-Status $statusCode $_.Exception.Message
}
Write-Host ""

# Тест 2: API Info
Write-Host "📊 Тест 2: API Info" -ForegroundColor $Blue
try {
    $response = Invoke-RestMethod -Uri "$ApiUrl/api-info" -Method Get
    Check-Status 200 $response
    
    Write-Host "📋 Имя: $($response.name)" -ForegroundColor $Green
    Write-Host "📋 Версия: $($response.version)" -ForegroundColor $Green
    Write-Host "📋 Возможности: $($response.capabilities.Count) функций" -ForegroundColor $Green
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Check-Status $statusCode $_.Exception.Message
}
Write-Host ""

# Тест 3: Создание проекта
Write-Host "📊 Тест 3: Создание проекта" -ForegroundColor $Blue
$projectData = @{
    name = "Тестовый жилой комплекс"
    project_type = "residential"
    location = "Москва, ул. Тестовая, 1"
    budget = 100000000
    area = 5000
    user_id = 1
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$ApiUrl/projects/" -Method Post -Body $projectData -ContentType "application/json"
    Check-Status 200 $response
    
    $projectId = $response.id
    Write-Host "📋 ID проекта: $projectId" -ForegroundColor $Green
    Write-Host "📋 Название: $($response.name)" -ForegroundColor $Green
    Write-Host "📋 Тип: $($response.project_type)" -ForegroundColor $Green
    Write-Host "📋 Бюджет: $($response.budget)" -ForegroundColor $Green
    
    # Сохраняем ID для следующих тестов
    $script:TestProjectId = $projectId
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Check-Status $statusCode $_.Exception.Message
    Write-Host "❌ Не удалось создать проект для дальнейших тестов" -ForegroundColor $Red
    exit 1
}
Write-Host ""

# Тест 4: Получение списка проектов
Write-Host "📊 Тест 4: Получение списка проектов" -ForegroundColor $Blue
try {
    $response = Invoke-RestMethod -Uri "$ApiUrl/projects/" -Method Get
    Check-Status 200 $response
    
    $projectsCount = $response.Count
    Write-Host "📋 Найдено проектов: $projectsCount" -ForegroundColor $Green
    
    if ($projectsCount -gt 0) {
        $firstProject = $response[0]
        Write-Host "📋 Первый проект: $($firstProject.name)" -ForegroundColor $Green
    }
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Check-Status $statusCode $_.Exception.Message
}
Write-Host ""

# Тест 5: Получение проекта по ID
if ($script:TestProjectId) {
    Write-Host "📊 Тест 5: Получение проекта по ID ($($script:TestProjectId))" -ForegroundColor $Blue
    try {
        $response = Invoke-RestMethod -Uri "$ApiUrl/projects/$($script:TestProjectId)" -Method Get
        Check-Status 200 $response
        
        Write-Host "📋 Название: $($response.name)" -ForegroundColor $Green
        Write-Host "📋 Локация: $($response.location)" -ForegroundColor $Green
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Check-Status $statusCode $_.Exception.Message
    }
    Write-Host ""
}

# Тест 6: Создание подрядчика
Write-Host "📊 Тест 6: Создание подрядчика" -ForegroundColor $Blue
$contractorData = @{
    name = "ООО Тестовый Подрядчик"
    specialization = "Жилое строительство"
    rating = 4.5
    contact_phone = "+7 (999) 123-45-67"
    contact_email = "test@contractor.ru"
    experience_years = 10
    completed_projects = 25
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$ApiUrl/contractors/" -Method Post -Body $contractorData -ContentType "application/json"
    Check-Status 200 $response
    
    Write-Host "📋 Название: $($response.name)" -ForegroundColor $Green
    Write-Host "📋 Специализация: $($response.specialization)" -ForegroundColor $Green
    Write-Host "📋 Рейтинг: $($response.rating)" -ForegroundColor $Green
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Check-Status $statusCode $_.Exception.Message
}
Write-Host ""

# Тест 7: Получение списка подрядчиков
Write-Host "📊 Тест 7: Получение списка подрядчиков" -ForegroundColor $Blue
try {
    $response = Invoke-RestMethod -Uri "$ApiUrl/contractors/" -Method Get
    Check-Status 200 $response
    
    $contractorsCount = $response.Count
    Write-Host "📋 Найдено подрядчиков: $contractorsCount" -ForegroundColor $Green
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Check-Status $statusCode $_.Exception.Message
}
Write-Host ""

# Тест 8: Получение простых сценариев
Write-Host "📊 Тест 8: Получение простых сценариев" -ForegroundColor $Blue
try {
    $response = Invoke-RestMethod -Uri "$ApiUrl/scenarios" -Method Get
    Check-Status 200 $response
    
    $scenariosCount = $response.Count
    Write-Host "📋 Найдено сценариев: $scenariosCount" -ForegroundColor $Green
    
    if ($scenariosCount -gt 0) {
        $firstScenario = $response[0]
        Write-Host "📋 Первый сценарий: $($firstScenario.name)" -ForegroundColor $Green
        Write-Host "📋 ROI: $($firstScenario.roi)%" -ForegroundColor $Green
    }
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Check-Status $statusCode $_.Exception.Message
}
Write-Host ""

# Тест 9: Генерация сценариев для проекта
if ($script:TestProjectId) {
    Write-Host "📊 Тест 9: Генерация сценариев для проекта ($($script:TestProjectId))" -ForegroundColor $Blue
    try {
        $response = Invoke-RestMethod -Uri "$ApiUrl/projects/$($script:TestProjectId)/scenarios/generate/?count=3" -Method Post
        Check-Status 200 $response
        
        $scenariosCount = $response.Count
        Write-Host "📋 Сгенерировано сценариев: $scenariosCount" -ForegroundColor $Green
        
        if ($scenariosCount -gt 0) {
            $firstScenario = $response[0]
            Write-Host "📋 Первый сценарий: $($firstScenario.name)" -ForegroundColor $Green
            Write-Host "📋 ROI: $($firstScenario.roi)%" -ForegroundColor $Green
        }
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Check-Status $statusCode $_.Exception.Message
    }
    Write-Host ""
}

# Тест 10: Статистика системы
Write-Host "📊 Тест 10: Статистика системы" -ForegroundColor $Blue
try {
    $response = Invoke-RestMethod -Uri "$ApiUrl/stats" -Method Get
    Check-Status 200 $response
    
    Write-Host "📋 Всего сценариев: $($response.scenarios.total_scenarios)" -ForegroundColor $Green
    Write-Host "📋 Всего пользователей: $($response.users.total_users)" -ForegroundColor $Green
    Write-Host "📋 Подрядчиков: $($response.contractors_count)" -ForegroundColor $Green
    Write-Host "📋 Отчетов: $($response.reports_generated)" -ForegroundColor $Green
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Check-Status $statusCode $_.Exception.Message
}
Write-Host ""

Write-Host "🎉 Тестирование завершено!" -ForegroundColor $Green
Write-Host "📋 Результаты сохранены в логах выше" -ForegroundColor $Blue 
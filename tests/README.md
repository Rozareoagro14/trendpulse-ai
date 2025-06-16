# Тесты TrendPulse AI

Этот каталог содержит юнит-тесты для проверки функциональности TrendPulse AI.

## 📁 Структура тестов

```
tests/
├── __init__.py                 # Пакет тестов
├── conftest.py                 # Конфигурация pytest и фикстуры
├── test_projects.py            # Тесты для проектов
├── test_scenarios.py           # Тесты для сценариев
├── test_contractors.py         # Тесты для подрядчиков
├── test_api_endpoints.py       # Тесты API endpoints
├── test_simple_project_creation.py  # Простые тесты без БД
├── requirements.txt            # Зависимости для тестов
└── README.md                   # Эта документация
```

## 🚀 Быстрый старт

### Вариант 1: Простые тесты (рекомендуется)

Запустите простые тесты, которые проверяют API без сложной настройки базы данных:

```bash
# На сервере (Linux/Mac)
chmod +x test_api.sh
./test_api.sh

# На Windows
powershell -ExecutionPolicy Bypass -File test_api.ps1
```

### Вариант 2: Python тесты

```bash
# Установка зависимостей
pip install -r tests/requirements.txt

# Запуск простых тестов
python run_tests.py --simple

# Запуск всех тестов
python run_tests.py --all

# Запуск с покрытием кода
python run_tests.py --coverage
```

## 📊 Что тестируется

### 1. Создание проектов
- ✅ Успешное создание проекта
- ✅ Валидация данных проекта
- ✅ Получение списка проектов
- ✅ Получение проекта по ID
- ✅ Создание нескольких проектов
- ✅ Валидация типов проектов
- ✅ Валидация бюджета

### 2. Сценарии
- ✅ Генерация сценариев для проекта
- ✅ Получение простых сценариев
- ✅ Генерация персонализированных сценариев
- ✅ Валидация данных сценариев
- ✅ Проверка расчета ROI
- ✅ Проверка стоимости
- ✅ Формат времени строительства

### 3. Подрядчики
- ✅ Создание подрядчика
- ✅ Валидация данных подрядчика
- ✅ Получение списка подрядчиков
- ✅ Валидация рейтинга
- ✅ Валидация опыта
- ✅ Валидация email и телефона

### 4. API Endpoints
- ✅ Health check
- ✅ API info
- ✅ Корневой endpoint
- ✅ Статистика системы
- ✅ Управление пользователями
- ✅ Обработка ошибок
- ✅ Пагинация

## 🔧 Настройка

### Переменные окружения

```bash
# URL API для тестирования
export API_URL="http://localhost:8000"

# Для тестов с базой данных
export TEST_DATABASE_URL="postgresql+asyncpg://test_user:test_password@localhost:5432/test_trendpulse"
```

### Зависимости

```bash
# Основные зависимости
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
pytest-cov==4.1.0
pytest-mock==3.12.0
```

## 📈 Покрытие кода

Для запуска тестов с покрытием кода:

```bash
python run_tests.py --coverage
```

Результаты будут сохранены в:
- `htmlcov/` - HTML отчет
- `coverage.xml` - XML отчет
- Консоль - краткий отчет

## 🐛 Отладка

### Просмотр логов

```bash
# Логи backend
docker-compose logs backend

# Логи bot
docker-compose logs bot

# Логи базы данных
docker-compose logs db
```

### Проверка статуса контейнеров

```bash
docker-compose ps
```

### Ручное тестирование API

```bash
# Health check
curl http://localhost:8000/health

# API info
curl http://localhost:8000/api-info

# Создание проекта
curl -X POST http://localhost:8000/projects/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Тестовый проект",
    "project_type": "residential_complex",
    "location": "Москва",
    "budget": 100000000,
    "area": 5000,
    "user_id": 12345
  }'
```

## 🎯 Цели тестирования

1. **Проверка создания проектов** - основная функциональность
2. **Валидация данных** - корректность входных данных
3. **API endpoints** - доступность и корректность ответов
4. **Интеграция** - взаимодействие между компонентами
5. **Обработка ошибок** - корректная обработка исключений

## 📝 Добавление новых тестов

1. Создайте новый файл `test_*.py`
2. Используйте существующие фикстуры из `conftest.py`
3. Добавьте тесты в соответствующий класс
4. Запустите тесты для проверки

Пример:

```python
import pytest
from httpx import AsyncClient

class TestNewFeature:
    @pytest.mark.asyncio
    async def test_new_feature(self, client: AsyncClient):
        response = await client.get("/new-endpoint")
        assert response.status_code == 200
```

## 🚨 Известные проблемы

1. **Тесты с базой данных** требуют настройки тестовой БД
2. **Асинхронные тесты** могут требовать настройки event loop
3. **Docker окружение** должно быть запущено для интеграционных тестов

## 📞 Поддержка

При возникновении проблем:

1. Проверьте статус контейнеров: `docker-compose ps`
2. Просмотрите логи: `docker-compose logs`
3. Запустите простые тесты: `./test_api.sh`
4. Проверьте подключение к API: `curl http://localhost:8000/health` 
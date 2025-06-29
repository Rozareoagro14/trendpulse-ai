# 🧪 Тестирование TrendPulse AI

## 📋 Обзор

Этот раздел содержит тесты для проверки функциональности TrendPulse AI системы.

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
pip install pytest pytest-asyncio httpx
```

### 2. Настройка тестовой базы данных
```bash
# Создание тестовой базы данных PostgreSQL
createdb test_trendpulse

# Создание тестового пользователя
psql -d test_trendpulse -c "CREATE USER test_user WITH PASSWORD '[ТЕСТОВЫЙ_ПАРОЛЬ]';"
psql -d test_trendpulse -c "GRANT ALL PRIVILEGES ON DATABASE test_trendpulse TO test_user;"
```

### 3. Запуск тестов
```bash
# Все тесты
pytest

# С подробным выводом
pytest -v

# С покрытием кода
pytest --cov=backend --cov=bot

# Конкретный тест
pytest tests/test_projects.py::test_create_project
```

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

## 🧪 Типы тестов

### 1. Unit тесты
- Тестирование отдельных функций
- Тестирование моделей данных
- Тестирование бизнес-логики

### 2. Integration тесты
- Тестирование API endpoints
- Тестирование взаимодействия с базой данных
- Тестирование полного цикла операций

### 3. API тесты
- Тестирование HTTP endpoints
- Проверка статус кодов
- Валидация ответов

## 📊 Примеры тестов

### Тест создания проекта
```python
async def test_create_project(client):
    """Тест создания нового проекта"""
    project_data = {
        "name": "Тестовый проект",
        "description": "Описание проекта",
        "project_type": "residential",
        "location": "Москва",
        "budget": 1000000,
        "area": 100
    }
    
    response = client.post("/projects/", json=project_data)
    assert response.status_code == 201
    
    project = response.json()
    assert project["name"] == project_data["name"]
    assert project["project_type"] == project_data["project_type"]
```

### Тест получения проектов
```python
async def test_get_projects(client):
    """Тест получения списка проектов"""
    response = client.get("/projects/")
    assert response.status_code == 200
    
    projects = response.json()
    assert isinstance(projects, list)
```

## 🔧 Конфигурация

### pytest.ini
```ini
[tool:pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### Переменные окружения для тестов
```bash
export TEST_DATABASE_URL="postgresql+asyncpg://test_user:[ТЕСТОВЫЙ_ПАРОЛЬ]@localhost:5432/test_trendpulse"
export TESTING=true
```

## 🚀 Запуск тестов в Docker

### 1. Создание тестового контейнера
```bash
docker run -d --name test-postgres \
  -e POSTGRES_DB=test_trendpulse \
  -e POSTGRES_USER=test_user \
  -e POSTGRES_PASSWORD=[ТЕСТОВЫЙ_ПАРОЛЬ] \
  -p 5433:5432 \
  postgres:15-alpine
```

### 2. Запуск тестов
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск тестов
pytest tests/ -v
```

## 📈 Покрытие кода

### Установка coverage
```bash
pip install pytest-cov
```

### Запуск с покрытием
```bash
pytest --cov=backend --cov=bot --cov-report=html
```

### Просмотр отчета
```bash
# Открыть HTML отчет
open htmlcov/index.html
```

## 🐛 Отладка тестов

### Подробный вывод
```bash
pytest -v -s --tb=long
```

### Остановка на первой ошибке
```bash
pytest -x
```

### Запуск конкретного теста
```bash
pytest tests/test_projects.py::test_create_project -v
```

## 📝 Написание новых тестов

### Структура теста
```python
import pytest
from httpx import AsyncClient

async def test_example(client: AsyncClient):
    """Описание теста"""
    # Arrange (подготовка)
    test_data = {...}
    
    # Act (действие)
    response = await client.post("/endpoint/", json=test_data)
    
    # Assert (проверка)
    assert response.status_code == 200
    assert response.json()["field"] == "expected_value"
```

### Фикстуры
```python
@pytest.fixture
def sample_project():
    """Фикстура с тестовым проектом"""
    return {
        "name": "Тестовый проект",
        "description": "Описание",
        "project_type": "residential",
        "location": "Москва",
        "budget": 1000000,
        "area": 100
    }
```

## 🔍 Мониторинг тестов

### Автоматический запуск
```bash
# Создание скрипта для автоматического тестирования
cat > run_tests.sh << 'EOF'
#!/bin/bash
echo "🧪 Запуск тестов TrendPulse AI..."
pytest tests/ -v --tb=short
echo "✅ Тесты завершены"
EOF

chmod +x run_tests.sh
```

### CI/CD интеграция
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_trendpulse
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: [ТЕСТОВЫЙ_ПАРОЛЬ]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio httpx
      - name: Run tests
        run: pytest tests/ -v
```

## 📊 Метрики качества

### Покрытие кода
- Цель: >80% покрытия
- Критические пути: 100%

### Время выполнения
- Unit тесты: <1 секунды
- Integration тесты: <5 секунд
- Полный набор: <30 секунд

### Надежность
- Все тесты должны проходить стабильно
- Отсутствие flaky тестов

## 🆘 Устранение неполадок

### Проблема: База данных недоступна
```bash
# Проверка статуса PostgreSQL
sudo systemctl status postgresql

# Проверка подключения
psql -h localhost -U test_user -d test_trendpulse
```

### Проблема: Тесты зависают
```bash
# Запуск с таймаутом
pytest tests/ --timeout=30

# Проверка процессов
ps aux | grep pytest
```

### Проблема: Ошибки импорта
```bash
# Проверка PYTHONPATH
echo $PYTHONPATH

# Установка в режиме разработки
pip install -e .
```

## 📚 Дополнительные ресурсы

- [pytest документация](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [httpx тестирование](https://www.python-httpx.org/async/)
- [SQLAlchemy тестирование](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites) 
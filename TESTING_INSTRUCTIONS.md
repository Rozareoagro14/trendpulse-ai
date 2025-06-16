# 🧪 Инструкции по тестированию TrendPulse AI

## 📋 Способы запуска тестов на сервере

### 🚀 Способ 1: Автоматические скрипты (рекомендуется)

#### Для Linux (bash):
```bash
# Подключитесь к серверу
ssh root@trashy-leg
cd /opt/trendpulse-ai

# Сделайте скрипт исполняемым и запустите
chmod +x run_tests_on_server.sh
./run_tests_on_server.sh
```

#### Для Windows (PowerShell):
```powershell
# Подключитесь к серверу
ssh root@trashy-leg
cd /opt/trendpulse-ai

# Запустите PowerShell скрипт
pwsh -File run_tests_on_server.ps1
```

### 🔍 Способ 2: Быстрое тестирование API

#### Для Linux:
```bash
chmod +x quick_api_test.sh
./quick_api_test.sh
```

#### Для Windows:
```powershell
pwsh -File quick_api_test.ps1
```

### 🐍 Способ 3: Ручной запуск pytest

#### Подготовка:
```bash
# Подключитесь к серверу
ssh root@trashy-leg
cd /opt/trendpulse-ai

# Установите зависимости для тестов
cd tests
pip install -r requirements.txt
```

#### Запуск отдельных тестов:
```bash
# Тест создания проектов
python -m pytest test_simple_project_creation.py -v

# Тест API endpoints
python -m pytest test_api_endpoints.py -v

# Тест подрядчиков
python -m pytest test_contractors.py -v

# Тест сценариев
python -m pytest test_scenarios.py -v

# Общие тесты проектов
python -m pytest test_projects.py -v
```

#### Запуск всех тестов:
```bash
# Из директории tests
python -m pytest -v

# Или из корневой директории
python -m pytest tests/ -v
```

## 📊 Что тестируется

### 1. **Создание проектов** (`test_simple_project_creation.py`)
- ✅ Создание проектов всех типов
- ✅ Валидация данных
- ✅ Привязка к пользователю
- ✅ Сохранение в базе данных

### 2. **API Endpoints** (`test_api_endpoints.py`)
- ✅ GET /health - здоровье API
- ✅ GET /projects/ - получение проектов
- ✅ POST /projects/ - создание проектов
- ✅ GET /contractors/ - получение подрядчиков
- ✅ GET /scenarios/ - получение сценариев
- ✅ GET /users/ - получение пользователей

### 3. **Подрядчики** (`test_contractors.py`)
- ✅ Получение списка подрядчиков
- ✅ Фильтрация по специализации
- ✅ Создание новых подрядчиков
- ✅ Обновление данных подрядчиков

### 4. **Сценарии** (`test_scenarios.py`)
- ✅ Генерация сценариев для проектов
- ✅ Расчет ROI, стоимости, времени
- ✅ Привязка к проектам
- ✅ Различные типы сценариев

### 5. **Общие тесты проектов** (`test_projects.py`)
- ✅ CRUD операции с проектами
- ✅ Фильтрация по пользователю
- ✅ Валидация бизнес-логики
- ✅ Интеграция с другими модулями

## 🎯 Ожидаемые результаты

### При успешном прохождении всех тестов:
```
🎉 =========================================
🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!
🎉 =========================================

📊 Система работает корректно:
   ✅ Создание проектов
   ✅ API endpoints
   ✅ Подрядчики
   ✅ Сценарии
   ✅ Общая функциональность
```

### При наличии ошибок:
```
⚠️  =========================================
⚠️  НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ
⚠️  =========================================

🔧 Рекомендации:
   1. Проверьте логи контейнеров
   2. Убедитесь, что база данных работает
   3. Проверьте подключение к API
   4. Запустите тесты повторно
```

## 🔧 Диагностика проблем

### Если тесты не запускаются:

#### 1. Проверьте статус контейнеров:
```bash
docker-compose ps
```

#### 2. Проверьте логи:
```bash
# Логи API
docker-compose logs backend

# Логи бота
docker-compose logs bot

# Логи базы данных
docker-compose logs db
```

#### 3. Проверьте API вручную:
```bash
# Проверка здоровья
curl http://localhost:8000/health

# Проверка проектов
curl http://localhost:8000/projects/

# Проверка подрядчиков
curl http://localhost:8000/contractors/
```

#### 4. Проверьте базу данных:
```bash
# Подключение к базе
docker-compose exec db psql -U postgres -d trendpulse

# Проверка таблиц
\dt

# Проверка данных
SELECT COUNT(*) FROM projects;
SELECT COUNT(*) FROM contractors;
SELECT COUNT(*) FROM scenarios;
```

### Если API не отвечает:

#### 1. Перезапустите контейнеры:
```bash
docker-compose restart
```

#### 2. Проверьте порты:
```bash
netstat -tlnp | grep 8000
```

#### 3. Проверьте переменные окружения:
```bash
docker-compose exec backend env | grep -E "(DATABASE|API)"
```

## 📋 Полезные команды

### Мониторинг системы:
```bash
# Статус контейнеров
docker-compose ps

# Использование ресурсов
docker stats

# Логи в реальном времени
docker-compose logs -f backend
docker-compose logs -f bot
```

### Управление тестами:
```bash
# Запуск с подробным выводом
python -m pytest -v -s

# Запуск конкретного теста
python -m pytest test_projects.py::test_create_project -v

# Запуск с покрытием кода
python -m pytest --cov=backend tests/

# Генерация отчета о покрытии
python -m pytest --cov=backend --cov-report=html tests/
```

### Очистка и перезапуск:
```bash
# Остановка всех контейнеров
docker-compose down

# Очистка кэша
docker system prune -f

# Перезапуск
docker-compose up -d

# Ожидание запуска
sleep 30
```

## 🎯 Рекомендации по тестированию

### 1. **Регулярное тестирование**
- Запускайте тесты после каждого обновления
- Проверяйте API перед деплоем
- Тестируйте новые функции

### 2. **Мониторинг производительности**
- Следите за временем ответа API
- Проверяйте использование ресурсов
- Анализируйте логи на ошибки

### 3. **Резервное копирование**
- Делайте бэкапы базы данных перед тестами
- Сохраняйте конфигурации
- Документируйте изменения

## ✅ Готово к тестированию!

Система полностью готова к тестированию. Выберите подходящий способ и запустите тесты для проверки работоспособности TrendPulse AI.

**Дата создания**: 16.06.2025
**Версия**: 3.0.0
**Статус**: ✅ Готово к тестированию 
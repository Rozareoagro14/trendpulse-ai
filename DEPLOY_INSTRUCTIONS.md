# Инструкции по деплою TrendPulse AI с тестированием

## 🚀 Быстрый деплой

### Вариант 1: Автоматический деплой (рекомендуется)

#### На Linux/Mac сервере:
```bash
# 1. Подключиться к серверу
ssh root@your-server-ip

# 2. Перейти в директорию проекта
cd /opt/trendpulse-ai

# 3. Сделать скрипт исполняемым и запустить
chmod +x deploy_with_tests.sh
./deploy_with_tests.sh
```

#### На Windows сервере:
```powershell
# 1. Подключиться к серверу
# 2. Перейти в директорию проекта
cd C:\opt\trendpulse-ai

# 3. Запустить PowerShell скрипт
powershell -ExecutionPolicy Bypass -File deploy_with_tests.ps1
```

### Вариант 2: Ручной деплой

```bash
# 1. Получить последние изменения
git pull origin main

# 2. Остановить контейнеры
docker-compose down

# 3. Пересобрать и запустить
docker-compose up --build -d

# 4. Подождать инициализации (60 секунд)
sleep 60

# 5. Проверить статус
docker-compose ps

# 6. Запустить тесты
chmod +x test_api.sh
./test_api.sh
```

## 📋 Что делает автоматический деплой

1. **📥 Обновление кода** - получает последние изменения из Git
2. **🛑 Остановка контейнеров** - останавливает текущие контейнеры
3. **🔨 Пересборка** - пересобирает образы с новым кодом
4. **🚀 Запуск** - запускает обновленные контейнеры
5. **⏳ Ожидание** - ждет инициализации системы (60 секунд)
6. **📊 Проверка** - проверяет статус контейнеров и логи
7. **🔍 Тестирование API** - проверяет доступность API
8. **🧪 Запуск тестов** - выполняет полное тестирование системы
9. **🎯 Финальная проверка** - показывает статистику и статус

## 🧪 Тестирование

### Запуск тестов вручную

```bash
# Простые тесты API
./test_api.sh

# Или PowerShell
.\test_api.ps1

# Python тесты (если установлен Python)
python run_tests.py --simple
```

### Что тестируется

- ✅ **Создание проектов** - основная функциональность
- ✅ **API endpoints** - доступность всех маршрутов
- ✅ **Валидация данных** - корректность входных данных
- ✅ **Сценарии** - генерация и получение сценариев
- ✅ **Подрядчики** - создание и управление подрядчиками
- ✅ **Статистика** - работа системы статистики

## 📊 Мониторинг

### Проверка статуса

```bash
# Статус контейнеров
docker-compose ps

# Логи backend
docker-compose logs -f backend

# Логи bot
docker-compose logs -f bot

# Логи базы данных
docker-compose logs -f db
```

### Проверка API

```bash
# Health check
curl http://localhost:8000/health

# API info
curl http://localhost:8000/api-info

# Статистика
curl http://localhost:8000/stats
```

### Проверка бота

1. Найдите бота в Telegram: `@trendpulse_aiv2_bot`
2. Отправьте `/start`
3. Создайте тестовый проект

## 🔧 Устранение неполадок

### Если контейнеры не запускаются

```bash
# Проверить логи
docker-compose logs

# Перезапустить с пересборкой
docker-compose down
docker-compose up --build -d

# Проверить порты
netstat -tulpn | grep 8000
```

### Если API недоступен

```bash
# Проверить статус backend
docker-compose ps backend

# Проверить логи backend
docker-compose logs backend

# Проверить переменные окружения
docker-compose exec backend env
```

### Если бот не отвечает

```bash
# Проверить статус bot
docker-compose ps bot

# Проверить логи bot
docker-compose logs bot

# Проверить подключение к API
docker-compose exec bot curl http://backend:8000/health
```

### Если тесты не проходят

```bash
# Проверить доступность API
curl http://localhost:8000/health

# Запустить тесты с подробным выводом
./test_api.sh 2>&1 | tee test_results.log

# Проверить логи контейнеров
docker-compose logs backend | tail -20
docker-compose logs bot | tail -20
```

## 📈 Результаты деплоя

После успешного деплоя вы должны увидеть:

```
🎉 Деплой завершен успешно!
📋 Система готова к работе
🔗 API: http://localhost:8000
🤖 Бот: @trendpulse_aiv2_bot
```

### Проверка работоспособности

1. **API доступен**: `curl http://localhost:8000/health` возвращает `{"status":"healthy"}`
2. **Бот работает**: отвечает на команду `/start` в Telegram
3. **Тесты проходят**: все тесты завершаются успешно
4. **Контейнеры запущены**: `docker-compose ps` показывает все контейнеры в статусе "Up"

## 🚨 Важные замечания

1. **Время инициализации**: система требует 60 секунд для полной инициализации
2. **Порты**: убедитесь, что порт 8000 свободен
3. **Переменные окружения**: проверьте файл `.env` с правильными настройками
4. **База данных**: PostgreSQL должна быть доступна
5. **Токен бота**: убедитесь, что токен бота корректный

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи: `docker-compose logs`
2. Запустите тесты: `./test_api.sh`
3. Проверьте статус: `docker-compose ps`
4. Перезапустите: `docker-compose restart`

## 🎯 Следующие шаги

После успешного деплоя:

1. **Протестируйте бота** в Telegram
2. **Создайте первый проект** через бота
3. **Проверьте генерацию сценариев**
4. **Настройте мониторинг** (опционально)
5. **Настройте резервное копирование** (опционально) 
# 🚀 Обновление TrendPulse AI - Исправление дублирования подрядчиков

## 📋 Что исправлено
- ✅ Добавлена дедупликация подрядчиков в боте
- ✅ Создан скрипт для добавления разнообразных подрядчиков
- ✅ Исправлено отображение дублированных подрядчиков

## 🔄 Команды для обновления

### 1. Подключитесь к серверу
```bash
ssh root@trashy-leg
cd /opt/trendpulse-ai
```

### 2. Получите последние изменения
```bash
git pull origin main
```

### 3. Перезапустите контейнеры
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 4. Добавьте разнообразных подрядчиков
```bash
# Установите зависимости для скрипта
pip install httpx

# Запустите скрипт добавления подрядчиков
python3 add_contractors.py
```

### 5. Проверьте результат
```bash
# Проверьте API подрядчиков
curl "http://localhost:8000/contractors/"

# Проверьте логи
docker-compose logs bot --tail=20
```

## 🧪 Тестирование

### Проверка в боте
1. Откройте бота в Telegram
2. Нажмите "👷 Подрядчики"
3. Должны показаться разные подрядчики без дублирования

## 📊 Ожидаемый результат
- В боте будут показаны 5 разных подрядчиков
- Не будет дублирования одного и того же подрядчика
- Каждый подрядчик будет иметь уникальные данные

## 🔧 Альтернативный способ добавления подрядчиков

Если скрипт не работает, можно добавить подрядчиков через API:

```bash
# Добавить первого подрядчика
curl -X POST "http://localhost:8000/contractors/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ООО СтройИнвест",
    "specialization": "Жилое строительство",
    "rating": 4.8,
    "contact_phone": "+7 (495) 123-45-67",
    "contact_email": "info@stroinvest.ru",
    "experience_years": 15,
    "completed_projects": 50
  }'

# Добавить второго подрядчика
curl -X POST "http://localhost:8000/contractors/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ООО КоммерцСтрой",
    "specialization": "Коммерческое строительство",
    "rating": 4.6,
    "contact_phone": "+7 (495) 234-56-78",
    "contact_email": "contact@commercstroy.ru",
    "experience_years": 12,
    "completed_projects": 35
  }'
```

## 📞 Поддержка
Если возникнут проблемы:
1. Проверьте логи: `docker-compose logs -f`
2. Проверьте API: `curl http://localhost:8000/health`
3. Проверьте подрядчиков: `curl http://localhost:8000/contractors/` 
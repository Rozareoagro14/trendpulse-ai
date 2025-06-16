# 🚀 Быстрый деплой на сервере

## ⚡ Одна команда для обновления

### Linux/Mac:
```bash
cd /opt/trendpulse-ai && chmod +x server_update.sh && ./server_update.sh
```

### Windows:
```powershell
cd C:\opt\trendpulse-ai; .\server_update.ps1
```

## 📋 Что произойдет:

1. 🛑 Остановка контейнеров
2. 📥 Обновление кода из Git
3. 🔨 Пересборка образов с новыми возможностями
4. ▶️ Запуск обновленных контейнеров
5. 📈 Генерация сценариев для всех проектов
6. ✅ Проверка работоспособности

## ✨ Новые возможности:

- 🎯 **Автоматическая генерация сценариев** при создании проекта
- 📊 **Интерактивный просмотр** с детальным анализом
- 🔄 **Генерация альтернатив** и PDF отчеты
- ⚡ **Быстрые обновления** с volumes

## 🎯 Проверка после деплоя:

```bash
# Статус
docker compose ps

# API
curl http://localhost:8000/health

# Бот работает
# Отправьте /start в @TrendPulseAI_bot
```

## 🚨 Если что-то пошло не так:

```bash
# Логи
docker compose logs

# Перезапуск
docker compose restart

# Полная пересборка
docker compose down && docker compose build --no-cache && docker compose up -d
```

**Готово! 🎉** 
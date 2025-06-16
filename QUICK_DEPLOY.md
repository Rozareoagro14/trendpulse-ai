# 🚀 Быстрый деплой TrendPulse AI

## На сервере выполните:

### Linux/Mac:
```bash
cd /opt/trendpulse-ai
chmod +x deploy_with_tests.sh
./deploy_with_tests.sh
```

### Windows:
```powershell
cd C:\opt\trendpulse-ai
powershell -ExecutionPolicy Bypass -File deploy_with_tests.ps1
```

## Что произойдет:

1. 📥 Обновление кода из Git
2. 🛑 Остановка контейнеров
3. 🔨 Пересборка с новым кодом
4. 🚀 Запуск обновленной системы
5. ⏳ Ожидание инициализации (60 сек)
6. 🧪 Автоматическое тестирование
7. ✅ Проверка работоспособности

## Результат:

- 🔗 API: http://localhost:8000
- 🤖 Бот: @trendpulse_aiv2_bot
- ✅ Все тесты пройдены
- 📊 Система готова к работе

## Если что-то пошло не так:

```bash
# Проверить статус
docker-compose ps

# Посмотреть логи
docker-compose logs

# Запустить тесты вручную
./test_api.sh
```

## Подробные инструкции:

См. файл `DEPLOY_INSTRUCTIONS.md` для детального описания процесса деплоя и устранения неполадок. 
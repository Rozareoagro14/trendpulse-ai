# 🚀 Быстрая переустановка TrendPulse AI

## 📋 Команды для выполнения на сервере

### 1. Подключитесь к серверу
```bash
ssh root@trashy-leg
```

### 2. Перейдите в директорию проекта
```bash
cd /opt/trendpulse-ai
```

### 3. Запустите автоматическую переустановку

**Вариант 1: Bash скрипт (рекомендуется)**
```bash
chmod +x fresh_deploy.sh
./fresh_deploy.sh
```

**Вариант 2: PowerShell скрипт**
```powershell
./fresh_deploy.ps1
```

**Вариант 3: Ручное выполнение**
```bash
# Сохраните .env
cp .env /tmp/trendpulse.env.backup

# Остановите и очистите все
docker-compose down
docker system prune -a -f

# Удалите старые файлы
cd /opt
rm -rf trendpulse-ai
mkdir trendpulse-ai
cd trendpulse-ai

# Восстановите .env и скачайте код
cp /tmp/trendpulse.env.backup .env
git clone https://github.com/Rozareoagro14/trendpulse-ai.git .

# Запустите систему
docker-compose build --no-cache
docker-compose up -d

# Проверьте работу
curl "http://localhost:8000/health"
```

## ✅ Что произойдет

1. ✅ Сохранится ваш .env файл
2. ✅ Удалятся все старые контейнеры и образы
3. ✅ Скачается свежий код из репозитория
4. ✅ Соберутся новые образы без кэша
5. ✅ Запустится система
6. ✅ Добавятся подрядчики (если возможно)
7. ✅ Проверится работа API

## 📱 После установки

Проверьте бота в Telegram:
- 📊 Мои проекты
- 👷 Подрядчики  
- 📈 Сценарии

## 🔧 Если что-то пошло не так

```bash
# Проверьте логи
docker-compose logs -f

# Проверьте статус
docker-compose ps

# Перезапустите
docker-compose restart
```

## 📞 Поддержка

Если нужна помощь - проверьте подробные инструкции в `FRESH_DEPLOYMENT.md` 
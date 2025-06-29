#!/usr/bin/expect -f

# Скрипт для автоматического подключения к серверу
# Использование: ./connect_server.sh

# Пароль сервера (замените на ваш)
PASSWORD="[ВАШ_ПАРОЛЬ_СЕРВЕРА]"

# Подключение к серверу
spawn ssh root@trashy-leg

# Ожидание запроса пароля
expect "password:"
send "$PASSWORD\r"

# Ожидание приглашения командной строки
expect "root@trashy-leg"

# Переход в директорию проекта
send "cd /opt/trendpulse-ai\r"

# Проверка статуса
send "docker-compose ps\r"

# Проверка API
send "curl -s http://localhost:8000/health\r"

# Переход в директорию проекта
send "cd /opt/trendpulse-ai\r"

# Создание .env файла с правильными настройками
send "cat > .env << 'EOF'\r"
send "# Telegram Bot Token\r"
send "BOT_TOKEN=[ВАШ_ТОКЕН_БОТА]\r"
send "\r"
send "# База данных\r"
send "DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/trendpulse\r"
send "\r"
send "# Окружение\r"
send "ENVIRONMENT=production\r"
send "\r"
send "# API URL (для бота)\r"
send "API_URL=http://backend:8000\r"
send "EOF\r"

# Перезапуск контейнеров
send "docker-compose restart\r"

# Проверка статуса после перезапуска
send "docker-compose ps\r"

# Проверка API после перезапуска
send "curl -s http://localhost:8000/health\r"

# Переход в интерактивный режим
interact 
-- Инициализация базы данных TrendPulse AI

-- Создание пользователя базы данных
CREATE USER trendpulse WITH PASSWORD '[ВАШ_ПАРОЛЬ_БАЗЫ]';

-- Создание базы данных
CREATE DATABASE trendpulse_db OWNER trendpulse;

-- Предоставление прав пользователю
GRANT ALL PRIVILEGES ON DATABASE trendpulse_db TO trendpulse;

-- Подключение к базе данных
\c trendpulse_db;

-- Создание расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Предоставление прав на схему public
GRANT ALL ON SCHEMA public TO trendpulse;

-- Создание таблиц (будут созданы автоматически через SQLAlchemy)
-- Таблицы создаются в backend/models.py

-- Настройка прав доступа
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO trendpulse;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO trendpulse; 
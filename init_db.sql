-- Создание пользователя и базы данных (с проверками)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'trendpulse') THEN
        CREATE USER trendpulse WITH PASSWORD 'trendpulse123';
    END IF;
END
$$;

-- Создание базы данных (если не существует)
SELECT 'CREATE DATABASE trendpulse_db OWNER trendpulse'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'trendpulse_db')\gexec

-- Подключение к созданной базе данных
\c trendpulse_db;

-- Предоставление прав на схему public
GRANT ALL ON SCHEMA public TO trendpulse;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO trendpulse;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO trendpulse;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO trendpulse;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO trendpulse; 
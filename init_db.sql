-- Создание пользователя и базы данных
CREATE USER trendpulse WITH PASSWORD 'trendpulse123';
CREATE DATABASE trendpulse_db OWNER trendpulse;
GRANT ALL PRIVILEGES ON DATABASE trendpulse_db TO trendpulse;

-- Подключение к созданной базе данных
\c trendpulse_db;

-- Предоставление прав на схему public
GRANT ALL ON SCHEMA public TO trendpulse;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO trendpulse;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO trendpulse; 
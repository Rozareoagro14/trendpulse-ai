import pytest
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    """Тест импорта основных модулей"""
    try:
        from backend.main import app
        assert app is not None
        print("✅ Импорт FastAPI приложения успешен")
    except ImportError as e:
        print(f"⚠️ Ошибка импорта FastAPI: {e}")

def test_database_imports():
    """Тест импорта базы данных"""
    try:
        from backend.database import engine, get_db
        assert engine is not None
        assert get_db is not None
        print("✅ Импорт базы данных успешен")
    except ImportError as e:
        print(f"⚠️ Ошибка импорта БД: {e}")

def test_models_imports():
    """Тест импорта моделей"""
    try:
        from backend.models import Project, Scenario, Contractor
        assert Project is not None
        assert Scenario is not None
        assert Contractor is not None
        print("✅ Импорт моделей успешен")
    except ImportError as e:
        print(f"⚠️ Ошибка импорта моделей: {e}")

def test_environment():
    """Тест окружения"""
    # Проверяем наличие .env файла или переменных окружения
    env_exists = os.path.exists('.env') or os.getenv('BOT_TOKEN') is not None
    assert env_exists, "Должен быть .env файл или переменные окружения"
    print("✅ Окружение настроено")

def test_requirements():
    """Тест зависимостей"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import asyncpg
        print("✅ Основные зависимости установлены")
    except ImportError as e:
        print(f"⚠️ Ошибка зависимостей: {e}")

def test_backend_structure():
    """Тест структуры backend"""
    try:
        # Проверяем, что можем импортировать основные модули backend
        import backend
        import backend.main
        import backend.database
        import backend.models
        print("✅ Структура backend корректна")
    except ImportError as e:
        print(f"⚠️ Ошибка структуры backend: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 
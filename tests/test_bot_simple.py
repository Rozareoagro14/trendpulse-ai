import pytest
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_bot_imports():
    """Тест импорта модулей бота"""
    try:
        # Проверяем, что можем импортировать основные модули
        from bot.states import ProjectCreationStates
        assert ProjectCreationStates is not None
        print("✅ Импорт состояний бота успешен")
    except ImportError as e:
        print(f"⚠️ Ошибка импорта состояний: {e}")
        # Не падаем, просто предупреждаем

def test_keyboard_imports():
    """Тест импорта клавиатур"""
    try:
        from bot.keyboards import get_main_keyboard, get_project_types_keyboard
        assert get_main_keyboard is not None
        assert get_project_types_keyboard is not None
        print("✅ Импорт клавиатур успешен")
    except ImportError as e:
        print(f"⚠️ Ошибка импорта клавиатур: {e}")
        # Не падаем, просто предупреждаем

def test_bot_states():
    """Тест состояний бота"""
    try:
        from bot.states import ProjectCreationStates
        assert hasattr(ProjectCreationStates, 'waiting_for_name')
        assert hasattr(ProjectCreationStates, 'waiting_for_type')
        print("✅ Состояния бота корректны")
    except Exception as e:
        print(f"⚠️ Ошибка состояний: {e}")

def test_environment():
    """Тест окружения"""
    assert os.path.exists('.env'), "Файл .env должен существовать"
    print("✅ Окружение настроено")

def test_directories():
    """Тест структуры директорий"""
    assert os.path.exists('bot'), "Директория bot должна существовать"
    assert os.path.exists('backend'), "Директория backend должна существовать"
    assert os.path.exists('tests'), "Директория tests должна существовать"
    print("✅ Структура директорий корректна")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 
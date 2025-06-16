import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bot.main import dp, bot
from bot.keyboards import get_main_keyboard, get_project_types_keyboard
from bot.states import ProjectCreationStates


@pytest.fixture
async def bot_instance():
    """Фикстура для создания экземпляра бота"""
    return bot


@pytest.fixture
async def dispatcher_instance():
    """Фикстура для создания диспетчера"""
    return dp


class TestBotKeyboards:
    """Тесты для клавиатур бота"""
    
    def test_main_keyboard(self):
        """Тест создания главной клавиатуры"""
        keyboard = get_main_keyboard()
        assert keyboard is not None
        assert hasattr(keyboard, 'inline_keyboard')
    
    def test_project_types_keyboard(self):
        """Тест создания клавиатуры типов проектов"""
        keyboard = get_project_types_keyboard()
        assert keyboard is not None
        assert hasattr(keyboard, 'inline_keyboard')


class TestBotStates:
    """Тесты для состояний бота"""
    
    def test_project_creation_states(self):
        """Тест состояний создания проекта"""
        assert ProjectCreationStates.waiting_for_name is not None
        assert ProjectCreationStates.waiting_for_type is not None


class TestBotInitialization:
    """Тесты инициализации бота"""
    
    def test_bot_creation(self, bot_instance):
        """Тест создания экземпляра бота"""
        assert bot_instance is not None
        assert hasattr(bot_instance, 'token')
    
    def test_dispatcher_creation(self, dispatcher_instance):
        """Тест создания диспетчера"""
        assert dispatcher_instance is not None


@pytest.mark.asyncio
async def test_bot_health_check():
    """Тест проверки здоровья бота"""
    # Простая проверка, что бот может быть создан
    assert bot is not None
    assert hasattr(bot, 'get_me')


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 
import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Импорты из нашего приложения
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.main import app
from backend.database import get_db
from backend.models import Base

# Тестовая база данных
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_password@localhost:5432/test_trendpulse"

# Создаем тестовый движок
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture(scope="session")
def event_loop():
    """Создает экземпляр стандартного event loop для тестовой сессии."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_db_setup():
    """Создает тестовую базу данных и таблицы."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(test_db_setup):
    """Создает новую сессию базы данных для каждого теста."""
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client(db_session):
    """Создает тестовый клиент FastAPI."""
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()

@pytest.fixture
def sample_project_data():
    """Возвращает тестовые данные для проекта."""
    return {
        "name": "Тестовый жилой комплекс",
        "project_type": "residential_complex",
        "location": "Москва, ул. Тестовая, 1",
        "budget": 100000000,
        "area": 5000,
        "user_id": 12345
    }

@pytest.fixture
def sample_contractor_data():
    """Возвращает тестовые данные для подрядчика."""
    return {
        "name": "ООО Тестовый Подрядчик",
        "specialization": "Жилое строительство",
        "rating": 4.5,
        "contact_phone": "+7 (999) 123-45-67",
        "contact_email": "test@contractor.ru",
        "experience_years": 10,
        "completed_projects": 25
    }

@pytest.fixture
def sample_user_data():
    """Возвращает тестовые данные для пользователя."""
    return {
        "telegram_id": 12345,
        "username": "test_user",
        "first_name": "Тест",
        "last_name": "Пользователь",
        "role": "investor"
    } 
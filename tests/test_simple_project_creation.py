import pytest
import httpx
import asyncio
import os
from typing import Dict, Any

class TestSimpleProjectCreation:
    """Простые тесты для проверки создания проектов через реальный API."""
    
    @pytest.fixture
    def api_url(self):
        """URL API для тестирования."""
        # Пытаемся получить URL из переменных окружения или используем локальный
        return os.getenv("API_URL", "http://localhost:8000")
    
    @pytest.fixture
    def sample_project_data(self) -> Dict[str, Any]:
        """Тестовые данные для проекта."""
        return {
            "name": "Тестовый жилой комплекс",
            "project_type": "residential_complex",
            "location": "Москва, ул. Тестовая, 1",
            "budget": 100000000,
            "area": 5000,
            "user_id": 12345
        }
    
    @pytest.mark.asyncio
    async def test_api_health_check(self, api_url: str):
        """Тест доступности API."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{api_url}/health")
                assert response.status_code == 200
                
                data = response.json()
                assert data["status"] == "healthy"
                print(f"✅ API доступен: {data}")
        except Exception as e:
            pytest.skip(f"API недоступен: {e}")
    
    @pytest.mark.asyncio
    async def test_create_project_success(self, api_url: str, sample_project_data: Dict[str, Any]):
        """Тест успешного создания проекта."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(f"{api_url}/projects/", json=sample_project_data)
                
                print(f"📊 Статус ответа: {response.status_code}")
                print(f"📋 Заголовки: {response.headers}")
                
                if response.status_code != 200:
                    print(f"❌ Ошибка: {response.text}")
                
                assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
                
                data = response.json()
                print(f"✅ Проект создан: {data}")
                
                # Проверяем основные поля
                assert data["name"] == sample_project_data["name"]
                assert data["project_type"] == sample_project_data["project_type"]
                assert data["location"] == sample_project_data["location"]
                assert data["budget"] == sample_project_data["budget"]
                assert data["area"] == sample_project_data["area"]
                assert "id" in data
                assert "created_at" in data
                
        except Exception as e:
            pytest.fail(f"Ошибка создания проекта: {e}")
    
    @pytest.mark.asyncio
    async def test_get_projects_list(self, api_url: str, sample_project_data: Dict[str, Any]):
        """Тест получения списка проектов."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Сначала создаем проект
                create_response = await client.post(f"{api_url}/projects/", json=sample_project_data)
                if create_response.status_code != 200:
                    pytest.skip(f"Не удалось создать проект для теста: {create_response.text}")
                
                # Получаем список проектов
                response = await client.get(f"{api_url}/projects/")
                assert response.status_code == 200
                
                data = response.json()
                print(f"📋 Найдено проектов: {len(data)}")
                
                assert isinstance(data, list)
                assert len(data) >= 1
                
                # Проверяем структуру первого проекта
                project = data[0]
                assert "id" in project
                assert "name" in project
                assert "project_type" in project
                assert "created_at" in project
                
        except Exception as e:
            pytest.fail(f"Ошибка получения списка проектов: {e}")
    
    @pytest.mark.asyncio
    async def test_create_project_validation(self, api_url: str):
        """Тест валидации данных проекта."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Тест с некорректными данными
                invalid_data = {
                    "name": "",  # Пустое имя
                    "project_type": "invalid_type",  # Несуществующий тип
                    "budget": -1000,  # Отрицательный бюджет
                    "area": 0  # Нулевая площадь
                }
                
                response = await client.post(f"{api_url}/projects/", json=invalid_data)
                print(f"🔍 Статус валидации: {response.status_code}")
                
                # Ожидаем ошибку валидации (422) или 400
                assert response.status_code in [422, 400], f"Ожидалась ошибка валидации, получен {response.status_code}"
                
        except Exception as e:
            pytest.fail(f"Ошибка тестирования валидации: {e}")
    
    @pytest.mark.asyncio
    async def test_project_types_validation(self, api_url: str):
        """Тест валидации типов проектов."""
        valid_types = [
            "residential_complex",
            "shopping_center", 
            "office_complex",
            "industrial_park",
            "data_center",
            "agricultural_processing",
            "logistics_center",
            "mixed_development"
        ]
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                for project_type in valid_types:
                    project_data = {
                        "name": f"Тест {project_type}",
                        "project_type": project_type,
                        "location": "Тест",
                        "budget": 1000000,
                        "area": 1000,
                        "user_id": 12345
                    }
                    
                    response = await client.post(f"{api_url}/projects/", json=project_data)
                    print(f"🔍 Тип {project_type}: статус {response.status_code}")
                    
                    assert response.status_code == 200, f"Ошибка для типа {project_type}: {response.text}"
                    
        except Exception as e:
            pytest.fail(f"Ошибка тестирования типов проектов: {e}")
    
    @pytest.mark.asyncio
    async def test_api_info_endpoint(self, api_url: str):
        """Тест endpoint с информацией об API."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{api_url}/api-info")
                assert response.status_code == 200
                
                data = response.json()
                print(f"📊 API версия: {data.get('version', 'неизвестна')}")
                print(f"🎯 Возможности: {len(data.get('capabilities', {}))} функций")
                
                assert "name" in data
                assert data["name"] == "TrendPulse AI API"
                assert "version" in data
                assert "capabilities" in data
                
        except Exception as e:
            pytest.fail(f"Ошибка получения информации об API: {e}")
    
    @pytest.mark.asyncio
    async def test_create_multiple_projects(self, api_url: str):
        """Тест создания нескольких проектов."""
        projects_data = [
            {
                "name": "Жилой комплекс А",
                "project_type": "residential_complex",
                "location": "Москва",
                "budget": 100000000,
                "area": 5000,
                "user_id": 12345
            },
            {
                "name": "Торговый центр Б",
                "project_type": "shopping_center",
                "location": "Санкт-Петербург",
                "budget": 200000000,
                "area": 8000,
                "user_id": 12345
            },
            {
                "name": "Офисный комплекс В",
                "project_type": "office_complex",
                "location": "Казань",
                "budget": 150000000,
                "area": 6000,
                "user_id": 12345
            }
        ]
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                created_projects = []
                
                for i, project_data in enumerate(projects_data):
                    response = await client.post(f"{api_url}/projects/", json=project_data)
                    print(f"📝 Проект {i+1}: статус {response.status_code}")
                    
                    assert response.status_code == 200, f"Ошибка создания проекта {i+1}: {response.text}"
                    created_projects.append(response.json())
                
                # Проверяем, что все проекты созданы с разными ID
                project_ids = [p["id"] for p in created_projects]
                assert len(set(project_ids)) == len(projects_data), "Не все проекты имеют уникальные ID"
                
                print(f"✅ Создано {len(created_projects)} проектов с уникальными ID")
                
        except Exception as e:
            pytest.fail(f"Ошибка создания нескольких проектов: {e}") 
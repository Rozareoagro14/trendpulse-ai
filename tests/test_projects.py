import pytest
from httpx import AsyncClient
from backend.models import Project, ProjectType
from backend.schemas import ProjectCreate, ProjectResponse

class TestProjects:
    """Тесты для работы с проектами."""
    
    @pytest.mark.asyncio
    async def test_create_project_success(self, client: AsyncClient, sample_project_data):
        """Тест успешного создания проекта."""
        response = await client.post("/projects/", json=sample_project_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Проверяем, что проект создан с правильными данными
        assert data["name"] == sample_project_data["name"]
        assert data["project_type"] == sample_project_data["project_type"]
        assert data["location"] == sample_project_data["location"]
        assert data["budget"] == sample_project_data["budget"]
        assert data["area"] == sample_project_data["area"]
        assert "id" in data
        assert "created_at" in data
        
    @pytest.mark.asyncio
    async def test_create_project_invalid_data(self, client: AsyncClient):
        """Тест создания проекта с некорректными данными."""
        invalid_data = {
            "name": "",  # Пустое имя
            "project_type": "invalid_type",  # Несуществующий тип
            "budget": -1000,  # Отрицательный бюджет
            "area": 0  # Нулевая площадь
        }
        
        response = await client.post("/projects/", json=invalid_data)
        assert response.status_code == 422  # Validation error
        
    @pytest.mark.asyncio
    async def test_get_projects_list(self, client: AsyncClient, sample_project_data):
        """Тест получения списка проектов."""
        # Создаем проект
        await client.post("/projects/", json=sample_project_data)
        
        # Получаем список проектов
        response = await client.get("/projects/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Проверяем структуру первого проекта
        project = data[0]
        assert "id" in project
        assert "name" in project
        assert "project_type" in project
        assert "created_at" in project
        
    @pytest.mark.asyncio
    async def test_get_project_by_id(self, client: AsyncClient, sample_project_data):
        """Тест получения проекта по ID."""
        # Создаем проект
        create_response = await client.post("/projects/", json=sample_project_data)
        project_id = create_response.json()["id"]
        
        # Получаем проект по ID
        response = await client.get(f"/projects/{project_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == project_id
        assert data["name"] == sample_project_data["name"]
        
    @pytest.mark.asyncio
    async def test_get_nonexistent_project(self, client: AsyncClient):
        """Тест получения несуществующего проекта."""
        response = await client.get("/projects/99999")
        assert response.status_code == 404
        
    @pytest.mark.asyncio
    async def test_create_multiple_projects(self, client: AsyncClient):
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
        
        created_projects = []
        for project_data in projects_data:
            response = await client.post("/projects/", json=project_data)
            assert response.status_code == 200
            created_projects.append(response.json())
        
        # Проверяем, что все проекты созданы с разными ID
        project_ids = [p["id"] for p in created_projects]
        assert len(set(project_ids)) == len(projects_data)
        
        # Проверяем, что все проекты в списке
        list_response = await client.get("/projects/")
        assert list_response.status_code == 200
        all_projects = list_response.json()
        assert len(all_projects) >= len(projects_data)
        
    @pytest.mark.asyncio
    async def test_project_types_validation(self, client: AsyncClient):
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
        
        for project_type in valid_types:
            project_data = {
                "name": f"Тест {project_type}",
                "project_type": project_type,
                "location": "Тест",
                "budget": 1000000,
                "area": 1000,
                "user_id": 12345
            }
            
            response = await client.post("/projects/", json=project_data)
            assert response.status_code == 200, f"Ошибка для типа {project_type}"
            
    @pytest.mark.asyncio
    async def test_project_budget_validation(self, client: AsyncClient):
        """Тест валидации бюджета проекта."""
        # Тест с очень большим бюджетом
        large_budget_data = {
            "name": "Мега проект",
            "project_type": "residential_complex",
            "location": "Москва",
            "budget": 1000000000000,  # 1 триллион
            "area": 100000,
            "user_id": 12345
        }
        
        response = await client.post("/projects/", json=large_budget_data)
        assert response.status_code == 200
        
        # Тест с нулевым бюджетом (должен быть отклонен)
        zero_budget_data = {
            "name": "Бесплатный проект",
            "project_type": "residential_complex",
            "location": "Москва",
            "budget": 0,
            "area": 1000,
            "user_id": 12345
        }
        
        response = await client.post("/projects/", json=zero_budget_data)
        assert response.status_code == 422  # Validation error
        
    @pytest.mark.asyncio
    async def test_get_projects_filtered_by_user(self, client: AsyncClient, sample_project_data):
        """Тест получения проектов с фильтрацией по пользователю."""
        # Создаем проект для первого пользователя
        project1_data = sample_project_data.copy()
        project1_data["user_id"] = 12345
        await client.post("/projects/", json=project1_data)
        
        # Создаем проект для второго пользователя
        project2_data = sample_project_data.copy()
        project2_data["name"] = "Проект пользователя 2"
        project2_data["user_id"] = 67890
        await client.post("/projects/", json=project2_data)
        
        # Получаем проекты первого пользователя
        response1 = await client.get("/projects/?user_id=12345")
        assert response1.status_code == 200
        projects1 = response1.json()
        assert len(projects1) == 1
        assert projects1[0]["user_id"] == 12345
        
        # Получаем проекты второго пользователя
        response2 = await client.get("/projects/?user_id=67890")
        assert response2.status_code == 200
        projects2 = response2.json()
        assert len(projects2) == 1
        assert projects2[0]["user_id"] == 67890
        
        # Получаем все проекты (без фильтра)
        response_all = await client.get("/projects/")
        assert response_all.status_code == 200
        all_projects = response_all.json()
        assert len(all_projects) >= 2 
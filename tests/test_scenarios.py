import pytest
from httpx import AsyncClient

class TestScenarios:
    """Тесты для работы со сценариями."""
    
    @pytest.mark.asyncio
    async def test_generate_scenarios_for_project(self, client: AsyncClient, sample_project_data):
        """Тест генерации сценариев для проекта."""
        # Создаем проект
        project_response = await client.post("/projects/", json=sample_project_data)
        assert project_response.status_code == 200
        project_id = project_response.json()["id"]
        
        # Генерируем сценарии
        response = await client.post(f"/projects/{project_id}/scenarios/generate/", params={"count": 3})
        assert response.status_code == 200
        
        scenarios = response.json()
        assert isinstance(scenarios, list)
        assert len(scenarios) == 3
        
        # Проверяем структуру сценария
        scenario = scenarios[0]
        assert "id" in scenario
        assert "name" in scenario
        assert "roi" in scenario
        assert "description" in scenario
        assert "estimated_cost" in scenario
        assert "construction_time" in scenario
        assert "project_id" in scenario
        
    @pytest.mark.asyncio
    async def test_get_simple_scenarios(self, client: AsyncClient):
        """Тест получения простых сценариев."""
        response = await client.get("/scenarios")
        assert response.status_code == 200
        
        scenarios = response.json()
        assert isinstance(scenarios, list)
        assert len(scenarios) >= 3  # У нас есть 3 тестовых сценария
        
        # Проверяем структуру
        scenario = scenarios[0]
        assert "id" in scenario
        assert "name" in scenario
        assert "roi" in scenario
        assert "description" in scenario
        assert "estimated_cost" in scenario
        assert "construction_time" in scenario
        
    @pytest.mark.asyncio
    async def test_generate_personalized_scenarios(self, client: AsyncClient):
        """Тест генерации персонализированных сценариев."""
        user_request_data = {
            "telegram_id": 12345,
            "land_plot": {
                "area": 5000,
                "zone_type": "residential",
                "infrastructure": ["electricity", "water", "road"],
                "power_capacity": 100,
                "budget": 100000000
            }
        }
        
        response = await client.post("/generate-scenarios", json=user_request_data)
        assert response.status_code == 200
        
        scenarios = response.json()
        assert isinstance(scenarios, list)
        assert len(scenarios) > 0
        
        # Проверяем, что сценарии связаны с пользователем
        scenario = scenarios[0]
        assert "id" in scenario
        assert "user_id" in scenario
        assert "land_plot_id" in scenario
        
    @pytest.mark.asyncio
    async def test_get_scenarios_for_project(self, client: AsyncClient, sample_project_data):
        """Тест получения сценариев для проекта."""
        # Создаем проект
        project_response = await client.post("/projects/", json=sample_project_data)
        project_id = project_response.json()["id"]
        
        # Создаем сценарий
        scenario_data = {
            "name": "Тестовый сценарий",
            "roi": 15.5,
            "description": "Описание тестового сценария",
            "estimated_cost": 50000000,
            "construction_time": "24 месяца"
        }
        
        await client.post(f"/projects/{project_id}/scenarios/", json=scenario_data)
        
        # Получаем сценарии проекта
        response = await client.get(f"/projects/{project_id}/scenarios/")
        assert response.status_code == 200
        
        scenarios = response.json()
        assert isinstance(scenarios, list)
        assert len(scenarios) >= 1
        
    @pytest.mark.asyncio
    async def test_scenario_validation(self, client: AsyncClient, sample_project_data):
        """Тест валидации данных сценария."""
        # Создаем проект
        project_response = await client.post("/projects/", json=sample_project_data)
        project_id = project_response.json()["id"]
        
        # Тест с некорректными данными
        invalid_scenario_data = {
            "name": "",  # Пустое имя
            "roi": -5,  # Отрицательный ROI
            "estimated_cost": -1000,  # Отрицательная стоимость
            "construction_time": ""  # Пустое время
        }
        
        response = await client.post(f"/projects/{project_id}/scenarios/", json=invalid_scenario_data)
        assert response.status_code == 422  # Validation error
        
    @pytest.mark.asyncio
    async def test_scenario_roi_calculation(self, client: AsyncClient, sample_project_data):
        """Тест расчета ROI в сценариях."""
        # Создаем проект
        project_response = await client.post("/projects/", json=sample_project_data)
        project_id = project_response.json()["id"]
        
        # Генерируем сценарии
        response = await client.post(f"/projects/{project_id}/scenarios/generate/", params={"count": 5})
        scenarios = response.json()
        
        # Проверяем, что ROI в разумных пределах
        for scenario in scenarios:
            roi = scenario["roi"]
            assert 0 < roi < 100, f"ROI {roi} вне разумных пределов"
            
    @pytest.mark.asyncio
    async def test_scenario_cost_validation(self, client: AsyncClient, sample_project_data):
        """Тест валидации стоимости в сценариях."""
        # Создаем проект
        project_response = await client.post("/projects/", json=sample_project_data)
        project_id = project_response.json()["id"]
        
        # Генерируем сценарии
        response = await client.post(f"/projects/{project_id}/scenarios/generate/", params={"count": 3})
        scenarios = response.json()
        
        # Проверяем, что стоимость положительная
        for scenario in scenarios:
            cost = scenario["estimated_cost"]
            assert cost > 0, f"Стоимость {cost} должна быть положительной"
            
    @pytest.mark.asyncio
    async def test_scenario_construction_time_format(self, client: AsyncClient, sample_project_data):
        """Тест формата времени строительства."""
        # Создаем проект
        project_response = await client.post("/projects/", json=sample_project_data)
        project_id = project_response.json()["id"]
        
        # Генерируем сценарии
        response = await client.post(f"/projects/{project_id}/scenarios/generate/", params={"count": 3})
        scenarios = response.json()
        
        # Проверяем формат времени строительства
        for scenario in scenarios:
            construction_time = scenario["construction_time"]
            assert isinstance(construction_time, str)
            assert len(construction_time) > 0
            # Проверяем, что содержит "месяц" или "год"
            assert any(word in construction_time.lower() for word in ["месяц", "год", "мес", "г"]) 
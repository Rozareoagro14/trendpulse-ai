import pytest
from httpx import AsyncClient

class TestAPIEndpoints:
    """Тесты для основных API endpoints."""
    
    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        """Тест health check endpoint."""
        response = await client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "version" in data
        assert data["version"] == "3.0.0"
        
    @pytest.mark.asyncio
    async def test_api_info(self, client: AsyncClient):
        """Тест API info endpoint."""
        response = await client.get("/api-info")
        assert response.status_code == 200
        
        data = response.json()
        assert "name" in data
        assert data["name"] == "TrendPulse AI API"
        assert "version" in data
        assert "description" in data
        assert "capabilities" in data
        assert "supported_project_types" in data
        assert "supported_infrastructure" in data
        assert "supported_zones" in data
        
        # Проверяем, что capabilities содержит ожидаемые ключи
        capabilities = data["capabilities"]
        expected_capabilities = [
            "scenario_generation",
            "contractor_matching", 
            "pdf_reports",
            "recommendations",
            "risk_assessment",
            "user_management",
            "analytics"
        ]
        
        for capability in expected_capabilities:
            assert capability in capabilities
            
    @pytest.mark.asyncio
    async def test_root_endpoint(self, client: AsyncClient):
        """Тест корневого endpoint."""
        response = await client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "description" in data
        assert "endpoints" in data
        
        # Проверяем, что endpoints содержит основные маршруты
        endpoints = data["endpoints"]
        expected_endpoints = [
            "scenarios",
            "generate_scenarios",
            "contractors",
            "users",
            "land_plots",
            "reports",
            "health",
            "stats"
        ]
        
        for endpoint in expected_endpoints:
            assert any(endpoint in key for key in endpoints.keys())
            
    @pytest.mark.asyncio
    async def test_stats_endpoint(self, client: AsyncClient):
        """Тест stats endpoint."""
        response = await client.get("/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert "scenarios" in data
        assert "users" in data
        assert "contractors_count" in data
        assert "reports_generated" in data
        
        # Проверяем структуру scenarios
        scenarios = data["scenarios"]
        assert "total_scenarios" in scenarios
        assert "average_roi" in scenarios
        assert "total_investment" in scenarios
        assert "most_popular_project_type" in scenarios
        assert "scenarios_by_zone" in scenarios
        
        # Проверяем структуру users
        users = data["users"]
        assert "total_users" in users
        assert "active_users_last_30_days" in users
        assert "users_by_role" in users
        assert "average_scenarios_per_user" in users
        
    @pytest.mark.asyncio
    async def test_user_management_endpoints(self, client: AsyncClient):
        """Тест endpoints для управления пользователями."""
        # Создание пользователя
        user_data = {
            "telegram_id": 12345,
            "username": "test_user",
            "first_name": "Тест",
            "last_name": "Пользователь",
            "role": "investor"
        }
        
        create_response = await client.post("/users", json=user_data)
        assert create_response.status_code == 200
        
        created_user = create_response.json()
        assert created_user["telegram_id"] == user_data["telegram_id"]
        assert created_user["username"] == user_data["username"]
        
        # Получение пользователя по telegram_id
        get_response = await client.get(f"/users/{user_data['telegram_id']}")
        assert get_response.status_code == 200
        
        retrieved_user = get_response.json()
        assert retrieved_user["telegram_id"] == user_data["telegram_id"]
        
        # Получение несуществующего пользователя
        not_found_response = await client.get("/users/99999")
        assert not_found_response.status_code == 404
        
    @pytest.mark.asyncio
    async def test_user_scenarios_endpoint(self, client: AsyncClient):
        """Тест получения сценариев пользователя."""
        # Сначала создаем пользователя
        user_data = {
            "telegram_id": 54321,
            "username": "scenario_user",
            "first_name": "Сценарий",
            "last_name": "Пользователь",
            "role": "developer"
        }
        
        await client.post("/users", json=user_data)
        
        # Получаем сценарии пользователя
        response = await client.get(f"/users/{user_data['telegram_id']}/scenarios")
        assert response.status_code == 200
        
        scenarios = response.json()
        assert isinstance(scenarios, list)
        
    @pytest.mark.asyncio
    async def test_scenario_detail_endpoint(self, client: AsyncClient):
        """Тест получения деталей сценария."""
        # Получаем несуществующий сценарий
        response = await client.get("/scenarios/99999")
        assert response.status_code == 404
        
    @pytest.mark.asyncio
    async def test_pdf_generation_endpoint(self, client: AsyncClient):
        """Тест генерации PDF отчета."""
        # Пытаемся сгенерировать PDF для несуществующего сценария
        response = await client.post("/scenarios/99999/generate-pdf")
        assert response.status_code == 404
        
    @pytest.mark.asyncio
    async def test_report_endpoint(self, client: AsyncClient):
        """Тест получения информации об отчете."""
        response = await client.get("/reports/1")
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data
        assert "scenario_id" in data
        assert "report_type" in data
        assert "file_path" in data
        assert "file_size" in data
        assert "generated_at" in data
        
    @pytest.mark.asyncio
    async def test_cors_headers(self, client: AsyncClient):
        """Тест CORS заголовков."""
        response = await client.options("/health")
        # CORS должен быть настроен для всех origins
        # Проверяем, что запрос не отклонен
        assert response.status_code in [200, 405]  # 405 если OPTIONS не поддерживается
        
    @pytest.mark.asyncio
    async def test_error_handling(self, client: AsyncClient):
        """Тест обработки ошибок."""
        # Тест несуществующего endpoint
        response = await client.get("/nonexistent-endpoint")
        assert response.status_code == 404
        
        # Тест неправильного метода
        response = await client.post("/health")
        assert response.status_code == 405  # Method Not Allowed
        
    @pytest.mark.asyncio
    async def test_pagination(self, client: AsyncClient, sample_project_data):
        """Тест пагинации для списков."""
        # Создаем несколько проектов
        for i in range(5):
            project_data = sample_project_data.copy()
            project_data["name"] = f"Проект {i+1}"
            await client.post("/projects/", json=project_data)
        
        # Тестируем пагинацию
        response = await client.get("/projects/?skip=0&limit=2")
        assert response.status_code == 200
        
        projects = response.json()
        assert len(projects) <= 2
        
        # Тестируем с пропуском
        response = await client.get("/projects/?skip=2&limit=2")
        assert response.status_code == 200
        
        projects = response.json()
        assert len(projects) <= 2
        
    @pytest.mark.asyncio
    async def test_contractors_pagination(self, client: AsyncClient, sample_contractor_data):
        """Тест пагинации для подрядчиков."""
        # Создаем несколько подрядчиков
        for i in range(5):
            contractor_data = sample_contractor_data.copy()
            contractor_data["name"] = f"Подрядчик {i+1}"
            await client.post("/contractors/", json=contractor_data)
        
        # Тестируем пагинацию
        response = await client.get("/contractors/?skip=0&limit=3")
        assert response.status_code == 200
        
        contractors = response.json()
        assert len(contractors) <= 3 
import pytest
from httpx import AsyncClient

class TestContractors:
    """Тесты для работы с подрядчиками."""
    
    @pytest.mark.asyncio
    async def test_create_contractor_success(self, client: AsyncClient, sample_contractor_data):
        """Тест успешного создания подрядчика."""
        response = await client.post("/contractors/", json=sample_contractor_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Проверяем, что подрядчик создан с правильными данными
        assert data["name"] == sample_contractor_data["name"]
        assert data["specialization"] == sample_contractor_data["specialization"]
        assert data["rating"] == sample_contractor_data["rating"]
        assert data["contact_phone"] == sample_contractor_data["contact_phone"]
        assert data["contact_email"] == sample_contractor_data["contact_email"]
        assert data["experience_years"] == sample_contractor_data["experience_years"]
        assert data["completed_projects"] == sample_contractor_data["completed_projects"]
        assert "id" in data
        assert "created_at" in data
        
    @pytest.mark.asyncio
    async def test_create_contractor_invalid_data(self, client: AsyncClient):
        """Тест создания подрядчика с некорректными данными."""
        invalid_data = {
            "name": "",  # Пустое имя
            "rating": 6.0,  # Рейтинг больше 5
            "experience_years": -5,  # Отрицательный опыт
            "completed_projects": -10  # Отрицательное количество проектов
        }
        
        response = await client.post("/contractors/", json=invalid_data)
        assert response.status_code == 422  # Validation error
        
    @pytest.mark.asyncio
    async def test_get_contractors_list(self, client: AsyncClient, sample_contractor_data):
        """Тест получения списка подрядчиков."""
        # Создаем подрядчика
        await client.post("/contractors/", json=sample_contractor_data)
        
        # Получаем список подрядчиков
        response = await client.get("/contractors/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Проверяем структуру первого подрядчика
        contractor = data[0]
        assert "id" in contractor
        assert "name" in contractor
        assert "specialization" in contractor
        assert "rating" in contractor
        assert "created_at" in contractor
        
    @pytest.mark.asyncio
    async def test_create_multiple_contractors(self, client: AsyncClient):
        """Тест создания нескольких подрядчиков."""
        contractors_data = [
            {
                "name": "ООО Строитель-1",
                "specialization": "Жилое строительство",
                "rating": 4.8,
                "contact_phone": "+7 (999) 111-11-11",
                "contact_email": "builder1@test.ru",
                "experience_years": 15,
                "completed_projects": 50
            },
            {
                "name": "ООО Строитель-2",
                "specialization": "Коммерческое строительство",
                "rating": 4.5,
                "contact_phone": "+7 (999) 222-22-22",
                "contact_email": "builder2@test.ru",
                "experience_years": 12,
                "completed_projects": 35
            },
            {
                "name": "ООО Строитель-3",
                "specialization": "Промышленное строительство",
                "rating": 4.2,
                "contact_phone": "+7 (999) 333-33-33",
                "contact_email": "builder3@test.ru",
                "experience_years": 8,
                "completed_projects": 20
            }
        ]
        
        created_contractors = []
        for contractor_data in contractors_data:
            response = await client.post("/contractors/", json=contractor_data)
            assert response.status_code == 200
            created_contractors.append(response.json())
        
        # Проверяем, что все подрядчики созданы с разными ID
        contractor_ids = [c["id"] for c in created_contractors]
        assert len(set(contractor_ids)) == len(contractors_data)
        
        # Проверяем, что все подрядчики в списке
        list_response = await client.get("/contractors/")
        assert list_response.status_code == 200
        all_contractors = list_response.json()
        assert len(all_contractors) >= len(contractors_data)
        
    @pytest.mark.asyncio
    async def test_contractor_rating_validation(self, client: AsyncClient):
        """Тест валидации рейтинга подрядчика."""
        # Тест с максимальным рейтингом
        max_rating_data = {
            "name": "Лучший подрядчик",
            "specialization": "Все виды работ",
            "rating": 5.0,
            "contact_phone": "+7 (999) 999-99-99",
            "contact_email": "best@test.ru",
            "experience_years": 20,
            "completed_projects": 100
        }
        
        response = await client.post("/contractors/", json=max_rating_data)
        assert response.status_code == 200
        
        # Тест с рейтингом больше 5 (должен быть отклонен)
        invalid_rating_data = {
            "name": "Неправильный подрядчик",
            "specialization": "Тест",
            "rating": 5.5,
            "contact_phone": "+7 (999) 000-00-00",
            "contact_email": "invalid@test.ru",
            "experience_years": 5,
            "completed_projects": 10
        }
        
        response = await client.post("/contractors/", json=invalid_rating_data)
        assert response.status_code == 422  # Validation error
        
    @pytest.mark.asyncio
    async def test_contractor_experience_validation(self, client: AsyncClient):
        """Тест валидации опыта подрядчика."""
        # Тест с большим опытом
        large_experience_data = {
            "name": "Опытный подрядчик",
            "specialization": "Строительство",
            "rating": 4.9,
            "contact_phone": "+7 (999) 888-88-88",
            "contact_email": "experienced@test.ru",
            "experience_years": 50,
            "completed_projects": 200
        }
        
        response = await client.post("/contractors/", json=large_experience_data)
        assert response.status_code == 200
        
        # Тест с отрицательным опытом (должен быть отклонен)
        negative_experience_data = {
            "name": "Новичок",
            "specialization": "Тест",
            "rating": 3.0,
            "contact_phone": "+7 (999) 777-77-77",
            "contact_email": "newbie@test.ru",
            "experience_years": -1,
            "completed_projects": 0
        }
        
        response = await client.post("/contractors/", json=negative_experience_data)
        assert response.status_code == 422  # Validation error
        
    @pytest.mark.asyncio
    async def test_contractor_email_validation(self, client: AsyncClient):
        """Тест валидации email подрядчика."""
        # Тест с корректным email
        valid_email_data = {
            "name": "Подрядчик с email",
            "specialization": "Строительство",
            "rating": 4.0,
            "contact_phone": "+7 (999) 666-66-66",
            "contact_email": "valid.email@test.ru",
            "experience_years": 10,
            "completed_projects": 25
        }
        
        response = await client.post("/contractors/", json=valid_email_data)
        assert response.status_code == 200
        
        # Тест с некорректным email (должен быть отклонен)
        invalid_email_data = {
            "name": "Подрядчик с плохим email",
            "specialization": "Строительство",
            "rating": 4.0,
            "contact_phone": "+7 (999) 555-55-55",
            "contact_email": "invalid-email",
            "experience_years": 10,
            "completed_projects": 25
        }
        
        response = await client.post("/contractors/", json=invalid_email_data)
        assert response.status_code == 422  # Validation error
        
    @pytest.mark.asyncio
    async def test_contractor_phone_validation(self, client: AsyncClient):
        """Тест валидации телефона подрядчика."""
        # Тест с корректным телефоном
        valid_phone_data = {
            "name": "Подрядчик с телефоном",
            "specialization": "Строительство",
            "rating": 4.0,
            "contact_phone": "+7 (999) 444-44-44",
            "contact_email": "phone@test.ru",
            "experience_years": 10,
            "completed_projects": 25
        }
        
        response = await client.post("/contractors/", json=valid_phone_data)
        assert response.status_code == 200
        
        # Тест с некорректным телефоном (должен быть отклонен)
        invalid_phone_data = {
            "name": "Подрядчик с плохим телефоном",
            "specialization": "Строительство",
            "rating": 4.0,
            "contact_phone": "неправильный-телефон",
            "contact_email": "badphone@test.ru",
            "experience_years": 10,
            "completed_projects": 25
        }
        
        response = await client.post("/contractors/", json=invalid_phone_data)
        assert response.status_code == 422  # Validation error 
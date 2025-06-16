from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import random
import os
from datetime import datetime

from .models import *
from .schemas import (
    UserCreate, ProjectCreate, ScenarioCreate, ContractorCreate,
    UserResponse, ProjectResponse, ScenarioResponse, ContractorResponse
)

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        user = User(**user_data.dict())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return UserResponse.model_validate(user)
    
    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_project(self, project_data: ProjectCreate) -> ProjectResponse:
        project = Project(**project_data.dict())
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return ProjectResponse.model_validate(project)
    
    async def get_projects(self, skip: int = 0, limit: int = 100) -> List[ProjectResponse]:
        result = await self.db.execute(
            select(Project).offset(skip).limit(limit)
        )
        projects = result.scalars().all()
        return [ProjectResponse.model_validate(project) for project in projects]
    
    async def get_project(self, project_id: int) -> Optional[ProjectResponse]:
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        project = result.scalar_one_or_none()
        return ProjectResponse.model_validate(project) if project else None

class ScenarioService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_scenario(self, project_id: int, scenario_data: ScenarioCreate) -> ScenarioResponse:
        scenario = Scenario(**scenario_data.dict(), project_id=project_id)
        self.db.add(scenario)
        await self.db.commit()
        await self.db.refresh(scenario)
        return ScenarioResponse.model_validate(scenario)
    
    async def get_scenarios(self, project_id: int) -> List[ScenarioResponse]:
        result = await self.db.execute(
            select(Scenario).where(Scenario.project_id == project_id)
        )
        scenarios = result.scalars().all()
        return [ScenarioResponse.model_validate(scenario) for scenario in scenarios]
    
    async def generate_scenarios(self, project_id: int, count: int = 3) -> List[ScenarioResponse]:
        """Генерирует сценарии развития для проекта"""
        project_result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        project = project_result.scalar_one_or_none()
        if not project:
            return []
        
        scenarios = []
        scenario_names = [
            "Консервативный сценарий",
            "Умеренный сценарий", 
            "Агрессивный сценарий",
            "Инновационный сценарий",
            "Экологичный сценарий"
        ]
        
        for i in range(min(count, len(scenario_names))):
            scenario_data = {
                "name": scenario_names[i],
                "description": f"Автоматически сгенерированный сценарий для проекта {project.name}",
                "roi": round(random.uniform(8.0, 35.0), 1),
                "estimated_cost": project.budget * random.uniform(0.8, 1.2) if project.budget else random.uniform(1000000, 50000000),
                "construction_time": f"{random.randint(12, 36)} месяцев",
                "risk_level": random.choice(["low", "medium", "high"]),
                "market_demand": random.choice(["low", "medium", "high"]),
                "regulatory_complexity": random.choice(["low", "medium", "high"])
            }
            
            scenario = Scenario(**scenario_data, project_id=project_id)
            self.db.add(scenario)
            scenarios.append(scenario)
        
        await self.db.commit()
        
        # Обновляем объекты для получения ID
        for scenario in scenarios:
            await self.db.refresh(scenario)
        
        return [ScenarioResponse.model_validate(scenario) for scenario in scenarios]

class ContractorService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_contractor(self, contractor_data: ContractorCreate) -> ContractorResponse:
        contractor = Contractor(**contractor_data.dict())
        self.db.add(contractor)
        await self.db.commit()
        await self.db.refresh(contractor)
        return ContractorResponse.model_validate(contractor)
    
    async def get_contractors(self, skip: int = 0, limit: int = 100) -> List[ContractorResponse]:
        result = await self.db.execute(
            select(Contractor).where(Contractor.is_active == True).offset(skip).limit(limit)
        )
        contractors = result.scalars().all()
        return [ContractorResponse.model_validate(contractor) for contractor in contractors]
    
    async def get_contractors_by_specialization(self, specializations: List[str]) -> List[ContractorResponse]:
        result = await self.db.execute(
            select(Contractor).where(
                Contractor.is_active == True,
                Contractor.specialization.in_(specializations)
            )
        )
        contractors = result.scalars().all()
        return [ContractorResponse.model_validate(contractor) for contractor in contractors]

class PDFService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def generate_project_pdf(self, project_id: int) -> Optional[str]:
        """Генерирует PDF отчет для проекта"""
        try:
            # Получаем проект
            project_result = await self.db.execute(
                select(Project).where(Project.id == project_id)
            )
            project = project_result.scalar_one_or_none()
            if not project:
                return None
            
            # Получаем сценарии
            scenarios_result = await self.db.execute(
                select(Scenario).where(Scenario.project_id == project_id)
            )
            scenarios = scenarios_result.scalars().all()
            
            # Создаем директорию для отчетов
            reports_dir = "/app/reports"
            os.makedirs(reports_dir, exist_ok=True)
            
            # Генерируем имя файла
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"project_{project_id}_{timestamp}.pdf"
            filepath = os.path.join(reports_dir, filename)
            
            # Здесь должна быть логика генерации PDF
            # Пока создаем простой текстовый файл
            with open(filepath.replace('.pdf', '.txt'), 'w', encoding='utf-8') as f:
                f.write(f"Отчет по проекту: {project.name}\n")
                f.write(f"Тип проекта: {project.project_type}\n")
                f.write(f"Локация: {project.location or 'Не указана'}\n")
                f.write(f"Бюджет: {project.budget or 'Не указан'}\n")
                f.write(f"Площадь: {project.area or 'Не указана'} кв.м\n")
                f.write(f"Дата создания: {project.created_at}\n\n")
                
                f.write("Сценарии развития:\n")
                for i, scenario in enumerate(scenarios, 1):
                    f.write(f"\n{i}. {scenario.name}\n")
                    f.write(f"   ROI: {scenario.roi}%\n")
                    f.write(f"   Стоимость: {scenario.estimated_cost}\n")
                    f.write(f"   Время строительства: {scenario.construction_time}\n")
                    f.write(f"   Уровень риска: {scenario.risk_level}\n")
            
            return filepath.replace('.pdf', '.txt')
            
        except Exception as e:
            print(f"Ошибка генерации PDF: {e}")
            return None 
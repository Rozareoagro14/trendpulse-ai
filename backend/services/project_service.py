from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.project import Project
from backend.schemas.project import ProjectCreate, ProjectResponse

class ProjectService:
    async def create_project(self, db: AsyncSession, project_data: ProjectCreate) -> ProjectResponse:
        """Создать новый проект"""
        # Создаем проект
        project = Project(**project_data.dict())
        db.add(project)
        await db.commit()
        await db.refresh(project)
        
        # Автоматически генерируем сценарии для нового проекта
        try:
            from backend.services.scenario_service import ScenarioService
            scenario_service = ScenarioService()
            await scenario_service.generate_scenarios(db, project.id, count=3)
        except Exception as e:
            # Логируем ошибку, но не прерываем создание проекта
            print(f"Ошибка автоматической генерации сценариев: {e}")
        
        return ProjectResponse(
            id=project.id,
            user_id=project.user_id,
            name=project.name,
            description=project.description,
            project_type=project.project_type,
            location=project.location,
            area=project.area,
            budget=project.budget,
            timeline=project.timeline,
            status=project.status,
            created_at=project.created_at,
            updated_at=project.updated_at
        )

    async def get_projects(self, db: AsyncSession, user_id: Optional[int] = None) -> List[ProjectResponse]:
        """Получить все проекты с фильтрацией по пользователю"""
        query = select(Project)
        if user_id:
            query = query.where(Project.user_id == user_id)
        
        result = await db.execute(query)
        projects = result.scalars().all()
        
        return [
            ProjectResponse(
                id=project.id,
                user_id=project.user_id,
                name=project.name,
                description=project.description,
                project_type=project.project_type,
                location=project.location,
                area=project.area,
                budget=project.budget,
                timeline=project.timeline,
                status=project.status,
                created_at=project.created_at,
                updated_at=project.updated_at
            )
            for project in projects
        ]

    async def get_project(self, db: AsyncSession, project_id: int) -> Optional[ProjectResponse]:
        """Получить проект по ID"""
        query = select(Project).where(Project.id == project_id)
        result = await db.execute(query)
        project = result.scalar_one_or_none()
        
        if project:
            return ProjectResponse(
                id=project.id,
                user_id=project.user_id,
                name=project.name,
                description=project.description,
                project_type=project.project_type,
                location=project.location,
                area=project.area,
                budget=project.budget,
                timeline=project.timeline,
                status=project.status,
                created_at=project.created_at,
                updated_at=project.updated_at
            )
        return None 
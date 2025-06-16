from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
from .models import User, Project, Scenario, Contractor, LandPlot, Report, UserSession, MarketData
from .schemas import UserCreate, ProjectCreate, ScenarioCreate, ContractorCreate

class UserCRUD:
    """CRUD операции для пользователей"""
    
    @staticmethod
    async def get_by_telegram_id(db: AsyncSession, telegram_id: int) -> Optional[User]:
        """Получить пользователя по Telegram ID"""
        result = await db.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create_user(db: AsyncSession, **kwargs) -> User:
        """Создать нового пользователя"""
        user = User(**kwargs)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def get_or_create_user(db: AsyncSession, telegram_id: int) -> User:
        """Получить существующего или создать нового пользователя"""
        user = await UserCRUD.get_by_telegram_id(db, telegram_id)
        if not user:
            user = await UserCRUD.create_user(db, telegram_id=telegram_id)
        return user

class LandPlotCRUD:
    """CRUD операции для земельных участков"""
    
    @staticmethod
    async def create_land_plot(db: AsyncSession, user_id: int, land_plot_data: Project) -> Project:
        """Создать новый земельный участок"""
        land_plot = Project(
            user_id=user_id,
            area=land_plot_data.area,
            zone_type=land_plot_data.zone_type.value,
            infrastructure=[infra.value for infra in land_plot_data.infrastructure],
            electricity_power=land_plot_data.electricity_power,
            gas_pressure=land_plot_data.gas_pressure,
            water_flow=land_plot_data.water_flow,
            road_access=land_plot_data.road_access,
            internet_available=land_plot_data.internet_available,
            location=land_plot_data.location if hasattr(land_plot_data, 'location') else None
        )
        db.add(land_plot)
        await db.commit()
        await db.refresh(land_plot)
        return land_plot
    
    @staticmethod
    async def get_user_land_plots(db: AsyncSession, user_id: int) -> List[LandPlot]:
        """Получить все участки пользователя"""
        result = await db.execute(
            select(LandPlot).where(LandPlot.user_id == user_id)
        )
        return result.scalars().all()

class ScenarioCRUD:
    """CRUD операции для сценариев"""
    
    @staticmethod
    async def create_scenario(db: AsyncSession, **kwargs) -> Scenario:
        """Создать новый сценарий"""
        scenario = Scenario(**kwargs)
        db.add(scenario)
        await db.commit()
        await db.refresh(scenario)
        return scenario
    
    @staticmethod
    async def get_scenario_by_id(db: AsyncSession, scenario_id: int) -> Optional[Scenario]:
        """Получить сценарий по ID"""
        result = await db.execute(
            select(Scenario).where(Scenario.id == scenario_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_scenarios(db: AsyncSession, user_id: int) -> List[Scenario]:
        """Получить все сценарии пользователя"""
        result = await db.execute(
            select(Scenario)
            .join(Project)
            .where(Project.user_id == user_id)
        )
        return result.scalars().all()

class ContractorCRUD:
    """CRUD операции для подрядчиков"""
    
    @staticmethod
    async def create_contractor(db: AsyncSession, **kwargs) -> Contractor:
        """Создать нового подрядчика"""
        contractor = Contractor(**kwargs)
        db.add(contractor)
        await db.commit()
        await db.refresh(contractor)
        return contractor
    
    @staticmethod
    async def get_all_active_contractors(db: AsyncSession) -> List[Contractor]:
        """Получить всех активных подрядчиков"""
        result = await db.execute(
            select(Contractor).where(Contractor.is_active == True)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_contractors_by_specialization(db: AsyncSession, specializations: List[str]) -> List[Contractor]:
        """Получить подрядчиков по специализации"""
        result = await db.execute(
            select(Contractor)
            .where(
                Contractor.is_active == True,
                Contractor.specialization.in_(specializations)
            )
        )
        return result.scalars().all()

class ReportCRUD:
    """CRUD операции для отчетов"""
    
    @staticmethod
    async def create_report(db: AsyncSession, scenario_id: int, report_type: str, 
                          file_path: str, file_size: Optional[int] = None) -> Report:
        """Создать новый отчет"""
        report = Report(
            scenario_id=scenario_id,
            report_type=report_type,
            file_path=file_path,
            file_size=file_size
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)
        return report
    
    @staticmethod
    async def get_scenario_reports(db: AsyncSession, scenario_id: int) -> List[Report]:
        """Получить все отчеты для сценария"""
        result = await db.execute(
            select(Report).where(Report.scenario_id == scenario_id)
        )
        return result.scalars().all()

class UserSessionCRUD:
    """CRUD операции для сессий пользователей"""
    
    @staticmethod
    async def get_session(db: AsyncSession, telegram_id: int) -> Optional[UserSession]:
        """Получить сессию пользователя"""
        result = await db.execute(
            select(UserSession).where(UserSession.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create_or_update_session(db: AsyncSession, telegram_id: int, 
                                     state: Optional[str] = None, 
                                     data: Optional[Dict] = None) -> UserSession:
        """Создать или обновить сессию пользователя"""
        session = await UserSessionCRUD.get_session(db, telegram_id)
        
        if session:
            # Обновляем существующую сессию
            if state is not None:
                session.state = state
            if data is not None:
                session.data = data
        else:
            # Создаем новую сессию
            session = UserSession(
                telegram_id=telegram_id,
                state=state,
                data=data
            )
            db.add(session)
        
        await db.commit()
        await db.refresh(session)
        return session
    
    @staticmethod
    async def delete_session(db: AsyncSession, telegram_id: int) -> bool:
        """Удалить сессию пользователя"""
        session = await UserSessionCRUD.get_session(db, telegram_id)
        if session:
            await db.delete(session)
            await db.commit()
            return True
        return False

class MarketDataCRUD:
    """CRUD операции для рыночных данных"""
    
    @staticmethod
    async def get_market_data(db: AsyncSession, region: str, 
                            project_type: str) -> Optional[MarketData]:
        """Получить рыночные данные"""
        result = await db.execute(
            select(MarketData).where(
                MarketData.region == region,
                MarketData.project_type == project_type
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create_market_data(db: AsyncSession, region: str, project_type: str,
                               construction_cost: float, rental_rate: float,
                               vacancy_rate: float, demand_score: float) -> MarketData:
        """Создать новые рыночные данные"""
        market_data = MarketData(
            region=region,
            project_type=project_type,
            construction_cost=construction_cost,
            rental_rate=rental_rate,
            vacancy_rate=vacancy_rate,
            demand_score=demand_score
        )
        db.add(market_data)
        await db.commit()
        await db.refresh(market_data)
        return market_data

class ProjectCRUD:
    """CRUD операции для проектов"""
    
    @staticmethod
    async def create_project(db: AsyncSession, **kwargs) -> Project:
        """Создать новый проект"""
        project = Project(**kwargs)
        db.add(project)
        await db.commit()
        await db.refresh(project)
        return project
    
    @staticmethod
    async def get_project_by_id(db: AsyncSession, project_id: int) -> Optional[Project]:
        """Получить проект по ID"""
        result = await db.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_projects(db: AsyncSession, user_id: int) -> List[Project]:
        """Получить все проекты пользователя"""
        result = await db.execute(
            select(Project).where(Project.user_id == user_id)
        )
        return result.scalars().all() 
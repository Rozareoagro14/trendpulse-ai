from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uvicorn
import os
from datetime import datetime
from dotenv import load_dotenv

from .database import get_db, engine
from .models import Base
from .schemas import (
    ProjectCreate, ProjectResponse, 
    ScenarioCreate, ScenarioResponse,
    ContractorCreate, ContractorResponse
)
from .services import (
    ProjectService, ScenarioService, 
    ContractorService, PDFService
)
from . import crud
from . import schemas

load_dotenv()

app = FastAPI(
    title="TrendPulse AI API",
    description="API для генерации сценариев развития и подбора подрядчиков",
    version="3.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация базы данных
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "3.0.0"}

# Проекты
@app.post("/projects/", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    service = ProjectService(db)
    return await service.create_project(project)

@app.get("/projects/", response_model=List[ProjectResponse])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    service = ProjectService(db)
    return await service.get_projects(skip=skip, limit=limit)

@app.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = ProjectService(db)
    project = await service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return project

# Сценарии
@app.post("/projects/{project_id}/scenarios/", response_model=ScenarioResponse)
async def create_scenario(
    project_id: int,
    scenario: ScenarioCreate,
    db: AsyncSession = Depends(get_db)
):
    service = ScenarioService(db)
    return await service.create_scenario(project_id, scenario)

@app.get("/projects/{project_id}/scenarios/", response_model=List[ScenarioResponse])
async def get_scenarios(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = ScenarioService(db)
    return await service.get_scenarios(project_id)

@app.post("/projects/{project_id}/scenarios/generate/", response_model=List[ScenarioResponse])
async def generate_scenarios(
    project_id: int,
    count: int = 3,
    db: AsyncSession = Depends(get_db)
):
    service = ScenarioService(db)
    return await service.generate_scenarios(project_id, count)

# Подрядчики
@app.post("/contractors/", response_model=ContractorResponse)
async def create_contractor(
    contractor: ContractorCreate,
    db: AsyncSession = Depends(get_db)
):
    service = ContractorService(db)
    return await service.create_contractor(contractor)

@app.get("/contractors/", response_model=List[ContractorResponse])
async def get_contractors(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    service = ContractorService(db)
    return await service.get_contractors(skip=skip, limit=limit)

# Генерация PDF
@app.post("/projects/{project_id}/generate-pdf/")
async def generate_pdf(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = PDFService(db)
    pdf_path = await service.generate_project_pdf(project_id)
    if not pdf_path:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return {"pdf_path": pdf_path, "message": "PDF успешно сгенерирован"}

@app.get("/")
async def root():
    return {
        "message": "TrendPulse AI API работает!",
        "version": "3.0.0",
        "description": "Цифровая экосистема девелопмента",
        "endpoints": {
            "scenarios": "/scenarios - Простые сценарии (для совместимости)",
            "generate_scenarios": "/generate-scenarios - Генерация персонализированных сценариев",
            "contractors": "/contractors - База подрядчиков",
            "users": "/users - Управление пользователями",
            "land_plots": "/land-plots - Управление участками",
            "reports": "/reports - Генерация PDF отчетов",
            "health": "/health - Проверка состояния",
            "stats": "/stats - Статистика системы"
        }
    }

@app.get("/scenarios", response_model=List[schemas.SimpleScenario])
async def get_scenarios():
    """Получить список простых сценариев (для обратной совместимости)"""
    return test_scenarios

@app.post("/generate-scenarios", response_model=List[schemas.ScenarioResponse])
async def generate_personalized_scenarios(
    user_request: schemas.UserRequestCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Генерирует персонализированные сценарии на основе параметров участка
    
    Это основной эндпоинт для создания сценариев с полной unit-экономикой,
    подбором подрядчиков и рекомендациями.
    """
    try:
        # Создаем или получаем пользователя
        user = await crud.UserCRUD.get_or_create_user(
            db, 
            user_request.telegram_id if hasattr(user_request, 'telegram_id') else 0
        )
        
        # Создаем земельный участок
        land_plot = await crud.LandPlotCRUD.create_land_plot(
            db, 
            user.id, 
            user_request.land_plot
        )
        
        # Генерируем сценарии
        scenarios = ScenarioService.generate_scenarios(
            user_request.land_plot, 
            user_request
        )
        
        # Сохраняем сценарии в базу данных
        saved_scenarios = []
        for scenario in scenarios:
            saved_scenario = await crud.ScenarioCRUD.create_scenario(
                db, 
                user.id, 
                land_plot.id, 
                scenario
            )
            saved_scenarios.append(saved_scenario)
        
        return saved_scenarios
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации сценариев: {str(e)}")

@app.get("/users/{telegram_id}", response_model=schemas.UserResponse)
async def get_user(telegram_id: int, db: AsyncSession = Depends(get_db)):
    """Получить пользователя по Telegram ID"""
    user = await crud.UserCRUD.get_by_telegram_id(db, telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@app.post("/users", response_model=schemas.UserResponse)
async def create_user(
    user_data: schemas.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать нового пользователя"""
    try:
        user = await crud.UserCRUD.create_user(db, **user_data.dict())
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания пользователя: {str(e)}")

@app.get("/users/{telegram_id}/scenarios", response_model=List[schemas.ScenarioResponse])
async def get_user_scenarios(telegram_id: int, db: AsyncSession = Depends(get_db)):
    """Получить все сценарии пользователя"""
    user = await crud.UserCRUD.get_by_telegram_id(db, telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    scenarios = await crud.ScenarioCRUD.get_user_scenarios(db, user.id)
    return scenarios

@app.get("/scenarios/{scenario_id}", response_model=schemas.ScenarioResponse)
async def get_scenario(scenario_id: int, db: AsyncSession = Depends(get_db)):
    """Получить сценарий по ID"""
    scenario = await crud.ScenarioCRUD.get_scenario_by_id(db, scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Сценарий не найден")
    return scenario

@app.post("/scenarios/{scenario_id}/generate-pdf")
async def generate_pdf_report(
    scenario_id: int,
    report_type: str = "pre_feasibility",
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    """Генерирует PDF отчет для сценария"""
    try:
        # Получаем сценарий
        scenario = await crud.ScenarioCRUD.get_scenario_by_id(db, scenario_id)
        if not scenario:
            raise HTTPException(status_code=404, detail="Сценарий не найден")
        
        # Получаем данные участка и пользователя
        land_plot = scenario.land_plot
        user = scenario.user
        
        # Генерируем PDF
        pdf_generator = PDFService()
        
        if report_type == "pre_feasibility":
            pdf_path = pdf_generator.generate_pre_feasibility_report(
                scenario_data=scenario.__dict__,
                land_plot_data=land_plot.__dict__,
                user_data=user.__dict__
            )
        elif report_type == "investment_memo":
            pdf_path = pdf_generator.generate_investment_memo(
                scenario_data=scenario.__dict__,
                land_plot_data=land_plot.__dict__,
                user_data=user.__dict__
            )
        else:
            raise HTTPException(status_code=400, detail="Неизвестный тип отчета")
        
        # Сохраняем информацию об отчете в базу
        report = await crud.ReportCRUD.create_report(
            db, 
            scenario_id, 
            report_type, 
            pdf_path,
            os.path.getsize(pdf_path) if os.path.exists(pdf_path) else None
        )
        
        return {
            "message": "PDF отчет успешно сгенерирован",
            "report_id": report.id,
            "filename": os.path.basename(pdf_path),
            "file_size": report.file_size,
            "download_url": f"/downloads/{report.id}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации PDF: {str(e)}")

@app.get("/reports/{report_id}", response_model=schemas.ReportResponse)
async def get_report(report_id: int, db: AsyncSession = Depends(get_db)):
    """Получить информацию об отчете"""
    # Здесь должна быть логика получения отчета из базы
    # Пока возвращаем заглушку
    return {
        "id": report_id,
        "scenario_id": 1,
        "report_type": "pre_feasibility",
        "file_path": f"/reports/report_{report_id}.pdf",
        "file_size": 1024000,
        "generated_at": datetime.now()
    }

@app.get("/stats", response_model=schemas.SystemStats)
async def get_system_stats(db: AsyncSession = Depends(get_db)):
    """Получить статистику системы"""
    # Здесь должна быть логика подсчета статистики
    # Пока возвращаем заглушку
    return {
        "scenarios": {
            "total_scenarios": 150,
            "average_roi": 18.5,
            "total_investment": 5000000000,
            "most_popular_project_type": "residential_complex",
            "scenarios_by_zone": {
                "residential": 45,
                "commercial": 35,
                "industrial": 40,
                "mixed": 30
            }
        },
        "users": {
            "total_users": 1200,
            "active_users_last_30_days": 450,
            "users_by_role": {
                "investor": 800,
                "developer": 300,
                "contractor": 100
            },
            "average_scenarios_per_user": 2.3
        },
        "contractors_count": 85,
        "reports_generated": 320
    }

@app.get("/api-info")
async def api_info():
    """Информация о возможностях API"""
    return {
        "name": "TrendPulse AI API",
        "version": "3.0.0",
        "description": "Цифровая экосистема девелопмента",
        "capabilities": {
            "scenario_generation": "Генерация персонализированных сценариев с unit-экономикой",
            "contractor_matching": "Подбор подходящих подрядчиков",
            "pdf_reports": "Генерация пред-ТЭО и инвестиционных меморандумов",
            "recommendations": "Умные рекомендации для улучшения проектов",
            "risk_assessment": "Оценка рисков и рыночного спроса",
            "user_management": "Управление пользователями и их данными",
            "analytics": "Статистика и аналитика системы"
        },
        "supported_project_types": [pt.value for pt in ProjectType],
        "supported_infrastructure": [it.value for it in InfrastructureType],
        "supported_zones": [zt.value for zt in ZoneType],
        "database": "PostgreSQL с async поддержкой",
        "pdf_generation": "WeasyPrint + Jinja2",
        "architecture": "FastAPI + SQLAlchemy + aiogram"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.services.scenario_service import ScenarioService
from backend.models.scenario import ScenarioResponse
from backend.database.database import get_db

router = APIRouter()
scenario_service = ScenarioService()

@router.get("/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(scenario_id: int, db: AsyncSession = Depends(get_db)):
    """Получить детальную информацию о сценарии"""
    scenario = await scenario_service.get_scenario(db, scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Сценарий не найден")
    return scenario 
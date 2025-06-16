from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.scenario import Scenario
from backend.schemas.scenario import ScenarioResponse

class ScenarioService:
    async def get_scenario(self, db: AsyncSession, scenario_id: int) -> Optional[ScenarioResponse]:
        """Получить сценарий по ID"""
        query = select(Scenario).where(Scenario.id == scenario_id)
        result = await db.execute(query)
        scenario = result.scalar_one_or_none()
        
        if scenario:
            return ScenarioResponse(
                id=scenario.id,
                project_id=scenario.project_id,
                name=scenario.name,
                description=scenario.description,
                estimated_cost=scenario.estimated_cost,
                roi=scenario.roi,
                construction_time=scenario.construction_time,
                risk_level=scenario.risk_level,
                payback_period=scenario.payback_period,
                net_profit=scenario.net_profit,
                planned_start_date=scenario.planned_start_date,
                risk_factors=scenario.risk_factors,
                risk_mitigation=scenario.risk_mitigation,
                market_demand=scenario.market_demand,
                competition_level=scenario.competition_level,
                price_trends=scenario.price_trends,
                area=scenario.area,
                floors=scenario.floors,
                materials=scenario.materials,
                technologies=scenario.technologies,
                created_at=scenario.created_at,
                updated_at=scenario.updated_at
            )
        return None 
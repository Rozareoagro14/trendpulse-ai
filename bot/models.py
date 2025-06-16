from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class InfrastructureType(str, Enum):
    """Типы инфраструктуры"""
    ELECTRICITY = "electricity"
    GAS = "gas"
    WATER = "water"
    SEWERAGE = "sewerage"
    ROAD = "road"
    INTERNET = "internet"

class ZoneType(str, Enum):
    """Типы зонирования"""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    AGRICULTURAL = "agricultural"
    MIXED = "mixed"

class LandPlot(BaseModel):
    """Модель земельного участка"""
    area: float = Field(..., description="Площадь участка в гектарах")
    zone_type: ZoneType = Field(..., description="Тип зонирования")
    infrastructure: List[InfrastructureType] = Field(default=[], description="Доступная инфраструктура")
    electricity_power: Optional[float] = Field(None, description="Мощность электричества в кВт")
    gas_pressure: Optional[float] = Field(None, description="Давление газа в МПа")
    water_flow: Optional[float] = Field(None, description="Расход воды в м³/час")
    road_access: Optional[bool] = Field(None, description="Наличие дорожного доступа")
    internet_available: Optional[bool] = Field(None, description="Наличие интернета")
    location: Optional[str] = Field(None, description="Местоположение участка")

class UserRequest(BaseModel):
    """Модель запроса пользователя"""
    telegram_id: int = Field(..., description="Telegram ID пользователя")
    land_plot: LandPlot = Field(..., description="Данные участка")
    investment_budget: Optional[float] = Field(None, description="Инвестиционный бюджет")
    project_type: Optional[str] = Field(None, description="Тип проекта")
    timeline: Optional[str] = Field(None, description="Временные рамки проекта")

class Scenario(BaseModel):
    """Модель сценария"""
    id: Optional[int] = Field(None, description="ID сценария")
    name: str = Field(..., description="Название сценария")
    description: str = Field(..., description="Описание сценария")
    roi: float = Field(..., description="ROI в процентах")
    investment_amount: float = Field(..., description="Сумма инвестиций")
    timeline_months: int = Field(..., description="Срок реализации в месяцах")
    risk_level: str = Field(..., description="Уровень риска")

class Contractor(BaseModel):
    """Модель подрядчика"""
    id: Optional[int] = Field(None, description="ID подрядчика")
    name: str = Field(..., description="Название компании")
    specialization: str = Field(..., description="Специализация")
    rating: float = Field(..., description="Рейтинг")
    experience_years: int = Field(..., description="Опыт работы в годах")
    contact_info: Optional[str] = Field(None, description="Контактная информация")
    is_active: bool = Field(True, description="Активен ли подрядчик")

class Project(BaseModel):
    """Модель проекта"""
    id: Optional[int] = Field(None, description="ID проекта")
    user_id: int = Field(..., description="ID пользователя")
    name: str = Field(..., description="Название проекта")
    land_plot: LandPlot = Field(..., description="Данные участка")
    status: str = Field("draft", description="Статус проекта")
    created_at: Optional[str] = Field(None, description="Дата создания")
    updated_at: Optional[str] = Field(None, description="Дата обновления") 
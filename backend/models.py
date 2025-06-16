from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class InfrastructureType(str, Enum):
    ELECTRICITY = "electricity"
    GAS = "gas"
    WATER = "water"
    SEWERAGE = "sewerage"
    ROAD = "road"
    INTERNET = "internet"

class ZoneType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    AGRICULTURAL = "agricultural"
    MIXED = "mixed"

class ProjectType(str, Enum):
    RESIDENTIAL_COMPLEX = "residential_complex"
    SHOPPING_CENTER = "shopping_center"
    OFFICE_COMPLEX = "office_complex"
    INDUSTRIAL_PARK = "industrial_park"
    DATA_CENTER = "data_center"
    AGRICULTURAL_PROCESSING = "agricultural_processing"
    LOGISTICS_CENTER = "logistics_center"
    MIXED_DEVELOPMENT = "mixed_development"

class LandPlot(BaseModel):
    area: float = Field(..., description="Площадь участка в гектарах")
    infrastructure: List[InfrastructureType] = Field(..., description="Доступная инфраструктура")
    zone_type: ZoneType = Field(..., description="Тип зонирования")
    electricity_power: Optional[float] = Field(None, description="Мощность электричества в МВт")
    gas_pressure: Optional[float] = Field(None, description="Давление газа в МПа")
    water_flow: Optional[float] = Field(None, description="Расход воды в м³/час")
    road_access: bool = Field(True, description="Наличие дорожного доступа")
    internet_available: bool = Field(False, description="Наличие интернета")

class UnitEconomics(BaseModel):
    total_investment: float = Field(..., description="Общие инвестиции в рублях")
    construction_cost: float = Field(..., description="Стоимость строительства")
    infrastructure_cost: float = Field(..., description="Стоимость инфраструктуры")
    operational_cost: float = Field(..., description="Операционные расходы в год")
    revenue_per_year: float = Field(..., description="Доход в год")
    roi_percentage: float = Field(..., description="ROI в процентах")
    payback_period: float = Field(..., description="Срок окупаемости в годах")
    npv: float = Field(..., description="Чистая приведенная стоимость")
    irr: float = Field(..., description="Внутренняя норма доходности")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    projects = relationship("Project", back_populates="user")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    project_type = Column(String(100), nullable=False)  # residential, commercial, mixed
    location = Column(String(200), nullable=True)
    budget = Column(Float, nullable=True)
    area = Column(Float, nullable=True)  # площадь в кв.м
    status = Column(String(50), default="draft")  # draft, active, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="projects")
    scenarios = relationship("Scenario", back_populates="project")

class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    roi = Column(Float, nullable=True)  # Return on Investment
    estimated_cost = Column(Float, nullable=True)
    construction_time = Column(String(100), nullable=True)
    risk_level = Column(String(50), nullable=True)  # low, medium, high
    market_demand = Column(String(50), nullable=True)  # low, medium, high
    regulatory_complexity = Column(String(50), nullable=True)  # low, medium, high
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    project = relationship("Project", back_populates="scenarios")

class Contractor(Base):
    __tablename__ = "contractors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    specialization = Column(String(200), nullable=False)
    experience_years = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)
    contact_phone = Column(String(20), nullable=True)
    contact_email = Column(String(100), nullable=True)
    website = Column(String(200), nullable=True)
    location = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    projects_completed = Column(Integer, default=0)
    average_rating = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Дополнительная информация в JSON формате
    additional_info = Column(JSON, nullable=True)

class DevelopmentScenario(BaseModel):
    id: int
    name: str
    project_type: ProjectType
    description: str
    land_requirements: LandPlot
    unit_economics: UnitEconomics
    construction_time: str
    risk_level: str = Field(..., description="Уровень риска")
    market_demand: str = Field(..., description="Рыночный спрос")
    regulatory_complexity: str = Field(..., description="Сложность регулирования")
    suitable_contractors: List[Contractor] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    pdf_template: str = Field(..., description="Шаблон для генерации PDF")

class UserRequest(BaseModel):
    land_plot: LandPlot
    investment_budget: Optional[float] = Field(None, description="Бюджет инвестиций")
    timeline: Optional[str] = Field(None, description="Желаемые сроки")
    risk_tolerance: Optional[str] = Field(None, description="Толерантность к риску")
    preferences: List[str] = Field(default_factory=list, description="Предпочтения пользователя") 
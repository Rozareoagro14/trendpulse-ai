from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from .models import InfrastructureType, ZoneType, ProjectType

# Схемы для запросов (Request)

class ProjectType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    MIXED = "mixed"
    INDUSTRIAL = "industrial"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class MarketDemand(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class UserBase(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

# Project schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    project_type: ProjectType
    location: Optional[str] = None
    budget: Optional[float] = None
    area: Optional[float] = None

class ProjectCreate(ProjectBase):
    user_id: int

class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

# Scenario schemas
class ScenarioBase(BaseModel):
    name: str
    description: Optional[str] = None
    roi: Optional[float] = None
    estimated_cost: Optional[float] = None
    construction_time: Optional[str] = None
    risk_level: Optional[RiskLevel] = None
    market_demand: Optional[MarketDemand] = None
    regulatory_complexity: Optional[RiskLevel] = None

class ScenarioCreate(ScenarioBase):
    pass

class ScenarioResponse(ScenarioBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    project_id: int
    created_at: datetime

# Contractor schemas
class ContractorBase(BaseModel):
    name: str
    specialization: str
    experience_years: Optional[int] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    projects_completed: Optional[int] = 0
    average_rating: Optional[float] = None
    additional_info: Optional[Dict[str, Any]] = None

class ContractorCreate(ContractorBase):
    pass

class ContractorResponse(ContractorBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime

# Simple schemas for backward compatibility
class SimpleScenario(BaseModel):
    id: int
    name: str
    roi: float
    description: str
    estimated_cost: float
    construction_time: str

class HealthCheck(BaseModel):
    status: str
    version: str
    database: Optional[str] = None
    services: Optional[Dict[str, str]] = None

# Схемы для статистики и аналитики

class ScenarioStats(BaseModel):
    total_scenarios: int
    average_roi: float
    total_investment: float
    most_popular_project_type: str
    scenarios_by_zone: Dict[str, int]

class UserStats(BaseModel):
    total_users: int
    active_users_last_30_days: int
    users_by_role: Dict[str, int]
    average_scenarios_per_user: float

class SystemStats(BaseModel):
    scenarios: ScenarioStats
    users: UserStats
    contractors_count: int
    reports_generated: int

# Схемы для фильтрации и поиска

class ScenarioFilter(BaseModel):
    min_roi: Optional[float] = None
    max_investment: Optional[float] = None
    project_type: Optional[str] = None
    zone_type: Optional[str] = None
    risk_level: Optional[str] = None

class ContractorFilter(BaseModel):
    specialization: Optional[List[str]] = None
    min_rating: Optional[float] = None
    price_range: Optional[str] = None
    location: Optional[str] = None

# Схемы для утилит

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime

class SuccessResponse(BaseModel):
    message: str
    data: Optional[Any] = None

# UserRequest schemas
class UserRequestCreate(BaseModel):
    land_plot: Dict[str, Any]
    investment_budget: Optional[float] = None
    timeline: Optional[str] = None
    risk_tolerance: Optional[str] = None
    preferences: Optional[List[str]] = None

class UserRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    land_plot: Dict[str, Any]
    investment_budget: Optional[float] = None
    timeline: Optional[str] = None
    risk_tolerance: Optional[str] = None
    preferences: Optional[List[str]] = None
    created_at: datetime 
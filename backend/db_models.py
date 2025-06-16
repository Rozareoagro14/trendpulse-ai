from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    role = Column(String(50), default="investor")  # investor, developer, contractor
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связи
    land_plots = relationship("LandPlot", back_populates="user")
    scenarios = relationship("Scenario", back_populates="user")

class LandPlot(Base):
    """Модель земельного участка"""
    __tablename__ = "land_plots"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    area = Column(Float, nullable=False)  # Площадь в гектарах
    zone_type = Column(String(50), nullable=False)  # residential, commercial, industrial, agricultural, mixed
    infrastructure = Column(JSON, nullable=False)  # Список доступной инфраструктуры
    electricity_power = Column(Float, nullable=True)  # Мощность электричества в МВт
    gas_pressure = Column(Float, nullable=True)  # Давление газа в МПа
    water_flow = Column(Float, nullable=True)  # Расход воды в м³/час
    road_access = Column(Boolean, default=True)
    internet_available = Column(Boolean, default=False)
    location = Column(String(200), nullable=True)  # Регион/город
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    user = relationship("User", back_populates="land_plots")
    scenarios = relationship("Scenario", back_populates="land_plot")

class Scenario(Base):
    """Модель сценария разработки"""
    __tablename__ = "scenarios"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    land_plot_id = Column(Integer, ForeignKey("land_plots.id"), nullable=False)
    name = Column(String(200), nullable=False)
    project_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Unit-экономика
    total_investment = Column(Float, nullable=False)
    construction_cost = Column(Float, nullable=False)
    infrastructure_cost = Column(Float, nullable=False)
    operational_cost = Column(Float, nullable=False)
    revenue_per_year = Column(Float, nullable=False)
    roi_percentage = Column(Float, nullable=False)
    payback_period = Column(Float, nullable=False)
    npv = Column(Float, nullable=False)
    irr = Column(Float, nullable=False)
    
    # Дополнительные параметры
    construction_time = Column(String(50), nullable=False)
    risk_level = Column(String(50), nullable=False)
    market_demand = Column(String(50), nullable=False)
    regulatory_complexity = Column(String(50), nullable=False)
    
    # Рекомендации и подрядчики
    recommendations = Column(JSON, nullable=True)  # Список рекомендаций
    suitable_contractors = Column(JSON, nullable=True)  # Список ID подрядчиков
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    user = relationship("User", back_populates="scenarios")
    land_plot = relationship("LandPlot", back_populates="scenarios")
    reports = relationship("Report", back_populates="scenario")

class Contractor(Base):
    """Модель подрядчика"""
    __tablename__ = "contractors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    specialization = Column(JSON, nullable=False)  # Список типов проектов
    rating = Column(Float, nullable=False)
    experience_years = Column(Integer, nullable=False)
    completed_projects = Column(Integer, nullable=False)
    price_range = Column(String(50), nullable=False)  # low, medium, high, premium
    contact_info = Column(JSON, nullable=False)  # {phone, email, website}
    portfolio = Column(JSON, nullable=True)  # Список ссылок на портфолио
    location = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Report(Base):
    """Модель отчета (PDF)"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False)
    report_type = Column(String(50), nullable=False)  # pre_feasibility, feasibility, investment
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=True)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    scenario = relationship("Scenario", back_populates="reports")

class MarketData(Base):
    """Модель рыночных данных"""
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    region = Column(String(100), nullable=False)
    project_type = Column(String(100), nullable=False)
    construction_cost_per_sqm = Column(Float, nullable=False)
    rental_rate_per_sqm = Column(Float, nullable=False)
    vacancy_rate = Column(Float, nullable=False)
    market_demand_score = Column(Float, nullable=False)  # 0-10
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

class UserSession(Base):
    """Модель сессии пользователя для FSM"""
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, nullable=False, index=True)
    state = Column(String(100), nullable=True)  # Текущее состояние FSM
    data = Column(JSON, nullable=True)  # Данные сессии
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 
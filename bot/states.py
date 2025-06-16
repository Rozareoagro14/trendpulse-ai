from aiogram.fsm.state import State, StatesGroup

class LandPlotForm(StatesGroup):
    """Состояния для сбора информации об участке"""
    waiting_for_area = State()
    waiting_for_zone = State()
    waiting_for_infrastructure = State()
    waiting_for_power = State()
    waiting_for_gas = State()
    waiting_for_water = State()
    waiting_for_location = State()
    waiting_for_budget = State()
    waiting_for_timeline = State()
    waiting_for_risk_tolerance = State()

class ScenarioForm(StatesGroup):
    """Состояния для работы со сценариями"""
    viewing_scenarios = State()
    viewing_scenario_detail = State()
    generating_pdf = State()
    viewing_contractors = State()

class UserProfileForm(StatesGroup):
    """Состояния для профиля пользователя"""
    editing_name = State()
    editing_phone = State()
    editing_role = State()

class ContractorForm(StatesGroup):
    """Состояния для работы с подрядчиками"""
    viewing_contractors = State()
    filtering_contractors = State()
    viewing_contractor_detail = State()

class ReportForm(StatesGroup):
    """Состояния для работы с отчетами"""
    selecting_report_type = State()
    generating_report = State()
    downloading_report = State()

class AdminForm(StatesGroup):
    """Состояния для административных функций"""
    adding_contractor = State()
    editing_contractor = State()
    viewing_statistics = State() 
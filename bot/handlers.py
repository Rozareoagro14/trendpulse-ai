import asyncio
import httpx
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from models import LandPlot, UserRequest, InfrastructureType, ZoneType

class LandPlotForm(StatesGroup):
    """Состояния для сбора информации об участке"""
    waiting_for_area = State()
    waiting_for_zone = State()
    waiting_for_infrastructure = State()
    waiting_for_power = State()
    waiting_for_budget = State()

class BotHandlers:
    """Обработчики для Telegram бота"""
    
    def __init__(self, api_url: str):
        self.api_url = api_url
    
    def get_main_keyboard(self):
        """Главная клавиатура"""
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="🏗️ Создать сценарий",
            callback_data="create_scenario"
        ))
        builder.add(InlineKeyboardButton(
            text="📊 Простые сценарии",
            callback_data="get_simple_scenarios"
        ))
        builder.add(InlineKeyboardButton(
            text="👷 Подрядчики",
            callback_data="get_contractors"
        ))
        builder.add(InlineKeyboardButton(
            text="ℹ️ О проекте",
            callback_data="about_project"
        ))
        return builder.as_markup()
    
    def get_zone_keyboard(self):
        """Клавиатура выбора зонирования"""
        builder = InlineKeyboardBuilder()
        zones = [
            ("🏠 Жилая", "residential"),
            ("🏢 Коммерческая", "commercial"),
            ("🏭 Промышленная", "industrial"),
            ("🌾 Сельхоз", "agricultural"),
            ("🏘️ Смешанная", "mixed")
        ]
        
        for name, zone in zones:
            builder.add(InlineKeyboardButton(
                text=name,
                callback_data=f"zone_{zone}"
            ))
        
        builder.adjust(2)  # 2 кнопки в ряд
        return builder.as_markup()
    
    def get_infrastructure_keyboard(self):
        """Клавиатура выбора инфраструктуры"""
        builder = InlineKeyboardBuilder()
        infrastructure = [
            ("⚡ Электричество", "electricity"),
            ("🔥 Газ", "gas"),
            ("💧 Вода", "water"),
            ("🚰 Канализация", "sewerage"),
            ("🛣️ Дороги", "road"),
            ("🌐 Интернет", "internet")
        ]
        
        for name, infra in infrastructure:
            builder.add(InlineKeyboardButton(
                text=name,
                callback_data=f"infra_{infra}"
            ))
        
        builder.adjust(2)
        return builder.as_markup()
    
    async def handle_start(self, message: types.Message):
        """Обработчик команды /start"""
        welcome_text = """
🚀 Добро пожаловать в TrendPulse AI!

Я помогу вам:
• Создать сценарии развития проектов
• Рассчитать unit-экономику
• Подобрать подрядчиков
• Сгенерировать отчеты

Выберите действие в меню ниже 👇
        """
        
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="🏗️ Создать проект")],
                [types.KeyboardButton(text="📊 Мои проекты")],
                [types.KeyboardButton(text="👷 Подрядчики")],
                [types.KeyboardButton(text="📈 Сценарии")],
                [types.KeyboardButton(text="ℹ️ Помощь")]
            ],
            resize_keyboard=True
        )
        
        await message.answer(welcome_text, reply_markup=keyboard)
    
    async def handle_create_scenario(self, callback: types.CallbackQuery, state: FSMContext):
        """Начало создания сценария"""
        await callback.answer()
        await callback.message.answer("Введите площадь участка в гектарах:")
        await state.set_state(LandPlotForm.waiting_for_area)
    
    async def handle_area_input(self, message: types.Message, state: FSMContext):
        """Обработка ввода площади участка"""
        try:
            area = float(message.text)
            await state.update_data(area=area)
            await message.answer("Площадь участка сохранена!")
        except ValueError:
            await message.answer("Пожалуйста, введите корректное число.")
    
    async def handle_zone_selection(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка выбора зонирования"""
        await callback.answer()
        zone = callback.data.replace("zone_", "")
        await state.update_data(zone_type=zone)
        await callback.message.answer(f"Выбрана зона: {zone}")
    
    async def handle_infrastructure_selection(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка выбора инфраструктуры"""
        await callback.answer()
        infra = callback.data.replace("infra_", "")
        await state.update_data(infrastructure=infra)
        await callback.message.answer(f"Выбрана инфраструктура: {infra}")
    
    async def handle_power_input(self, message: types.Message, state: FSMContext):
        """Обработка ввода мощности электричества"""
        try:
            power = float(message.text)
            await state.update_data(electricity_power=power)
            await message.answer("Мощность электричества сохранена!")
        except ValueError:
            await message.answer("Пожалуйста, введите корректное число.")
    
    async def handle_budget_input(self, message: types.Message, state: FSMContext):
        """Обработка ввода бюджета"""
        try:
            budget = float(message.text)
            await state.update_data(investment_budget=budget)
            await message.answer("Бюджет сохранен!")
        except ValueError:
            await message.answer("Пожалуйста, введите корректную сумму.")
    
    async def handle_simple_scenarios(self, callback: types.CallbackQuery):
        """Показ простых сценариев"""
        await callback.answer()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}/scenarios")
                if response.status_code == 200:
                    scenarios = response.json()
                    text = "📊 Доступные сценарии:\n\n"
                    for scenario in scenarios:
                        text += f"🏗️ {scenario['name']}\n"
                        text += f"💰 ROI: {scenario['roi']}%\n"
                        text += f"📝 {scenario['description']}\n\n"
                    await callback.message.answer(text)
                else:
                    await callback.message.answer("Ошибка получения сценариев")
        except Exception as e:
            await callback.message.answer(f"Ошибка: {e}")
    
    async def handle_contractors(self, callback: types.CallbackQuery):
        """Показ подрядчиков"""
        await callback.answer()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}/contractors")
                if response.status_code == 200:
                    contractors = response.json()
                    text = "👷 Доступные подрядчики:\n\n"
                    for contractor in contractors[:5]:
                        text += f"🏢 {contractor['name']}\n"
                        text += f"🎯 {contractor['specialization']}\n"
                        text += f"⭐ Рейтинг: {contractor['rating']}\n\n"
                    await callback.message.answer(text)
                else:
                    await callback.message.answer("Ошибка получения подрядчиков")
        except Exception as e:
            await callback.message.answer(f"Ошибка: {e}")
    
    async def handle_about_project(self, callback: types.CallbackQuery):
        """Информация о проекте"""
        await callback.answer()
        about_text = """
📋 TrendPulse AI v3.0.0

🎯 Цель проекта:
Создание цифровой экосистемы для девелоперов и инвесторов в сфере недвижимости.

🚀 Возможности:
• Генерация сценариев развития
• Расчет unit-экономики
• Подбор подрядчиков
• Генерация PDF отчетов
• Анализ рисков и спроса

💻 Технологии:
• Backend: FastAPI + SQLAlchemy
• Bot: aiogram 3.x
• Database: PostgreSQL
• PDF: WeasyPrint + Jinja2

🔗 API: http://backend:8000
📚 Документация: /docs
        """
        await callback.message.answer(about_text) 
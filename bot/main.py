import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import httpx
from dotenv import load_dotenv

from handlers import BotHandlers, LandPlotForm

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL", "http://backend:8000")

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Создаем экземпляр обработчиков
handlers = BotHandlers(API_URL)

# Состояния FSM
class ProjectStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_type = State()
    waiting_for_location = State()
    waiting_for_budget = State()
    waiting_for_area = State()

class UserStates(StatesGroup):
    waiting_for_phone = State()
    waiting_for_email = State()

# Клавиатуры
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏗️ Создать проект")],
            [KeyboardButton(text="📊 Мои проекты")],
            [KeyboardButton(text="👷 Подрядчики")],
            [KeyboardButton(text="📈 Сценарии")],
            [KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_project_type_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏠 Жилой")],
            [KeyboardButton(text="🏢 Коммерческий")],
            [KeyboardButton(text="🏭 Промышленный")],
            [KeyboardButton(text="🏘️ Смешанный")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_back_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Назад")]],
        resize_keyboard=True
    )
    return keyboard

# Регистрируем обработчики
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    await handlers.handle_start(message)

@dp.callback_query(lambda c: c.data == "create_scenario")
async def process_create_scenario(callback: types.CallbackQuery, state):
    """Начало создания сценария"""
    await handlers.handle_create_scenario(callback, state)

@dp.message(LandPlotForm.waiting_for_area)
async def process_area_input(message: types.Message, state):
    """Обработка ввода площади участка"""
    await handlers.handle_area_input(message, state)

@dp.callback_query(lambda c: c.data.startswith("zone_"))
async def process_zone_selection(callback: types.CallbackQuery, state):
    """Обработка выбора зонирования"""
    await handlers.handle_zone_selection(callback, state)

@dp.callback_query(lambda c: c.data.startswith("infra_"))
async def process_infrastructure_selection(callback: types.CallbackQuery, state):
    """Обработка выбора инфраструктуры"""
    await handlers.handle_infrastructure_selection(callback, state)

@dp.message(LandPlotForm.waiting_for_power)
async def process_power_input(message: types.Message, state):
    """Обработка ввода мощности электричества"""
    await handlers.handle_power_input(message, state)

@dp.message(LandPlotForm.waiting_for_budget)
async def process_budget_input(message: types.Message, state):
    """Обработка ввода бюджета"""
    await handlers.handle_budget_input(message, state)

@dp.callback_query(lambda c: c.data == "get_simple_scenarios")
async def process_simple_scenarios(callback: types.CallbackQuery):
    """Показ простых сценариев"""
    await handlers.handle_simple_scenarios(callback)

@dp.callback_query(lambda c: c.data == "get_contractors")
async def process_contractors(callback: types.CallbackQuery):
    """Показ подрядчиков"""
    await handlers.handle_contractors(callback)

@dp.callback_query(lambda c: c.data == "about_project")
async def process_about_project(callback: types.CallbackQuery):
    """Информация о проекте"""
    await handlers.handle_about_project(callback)

@dp.callback_query(lambda c: c.data.startswith('scenario_detail_'))
async def show_scenario_detail(callback_query: types.CallbackQuery):
    try:
        scenario_id = int(callback_query.data.split('_')[2])
        
        async with httpx.AsyncClient() as client:
            # Получаем детальную информацию о сценарии
            scenario_response = await client.get(f"{API_URL}/scenarios/{scenario_id}")
            
            if scenario_response.status_code == 200:
                scenario = scenario_response.json()
                
                # Получаем информацию о проекте
                project_response = await client.get(f"{API_URL}/projects/{scenario['project_id']}")
                project = project_response.json() if project_response.status_code == 200 else None
                
                # Формируем детальное описание сценария
                detail_text = f"📊 Детальный анализ сценария\n\n"
                detail_text += f"🏗️ Проект: {project['name'] if project else 'Неизвестно'}\n"
                detail_text += f"📋 Название: {scenario['name']}\n\n"
                
                detail_text += f"💰 Финансовые показатели:\n"
                detail_text += f"  • ROI: {scenario['roi']}%\n"
                detail_text += f"  • Стоимость: {scenario['estimated_cost']:,.0f} ₽\n"
                detail_text += f"  • Срок окупаемости: {scenario['payback_period']} лет\n"
                detail_text += f"  • Чистая прибыль: {scenario['net_profit']:,.0f} ₽\n\n"
                
                detail_text += f"⏱️ Временные параметры:\n"
                detail_text += f"  • Срок строительства: {scenario['construction_time']}\n"
                detail_text += f"  • Планируемый запуск: {scenario['planned_start_date']}\n\n"
                
                detail_text += f"⚠️ Риски и особенности:\n"
                detail_text += f"  • Уровень риска: {scenario['risk_level']}\n"
                detail_text += f"  • Основные риски: {scenario['risk_factors']}\n"
                detail_text += f"  • Меры по снижению рисков: {scenario['risk_mitigation']}\n\n"
                
                detail_text += f"📈 Рыночные факторы:\n"
                detail_text += f"  • Рыночный спрос: {scenario['market_demand']}\n"
                detail_text += f"  • Конкуренция: {scenario['competition_level']}\n"
                detail_text += f"  • Ценовые тренды: {scenario['price_trends']}\n\n"
                
                detail_text += f"🔧 Технические детали:\n"
                detail_text += f"  • Площадь: {scenario['area']} м²\n"
                detail_text += f"  • Этажность: {scenario['floors']}\n"
                detail_text += f"  • Материалы: {scenario['materials']}\n"
                detail_text += f"  • Технологии: {scenario['technologies']}\n\n"
                
                detail_text += f"📝 Дополнительная информация:\n"
                detail_text += f"{scenario['description']}\n\n"
                
                # Создаем клавиатуру с действиями
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="📊 Создать отчет PDF",
                            callback_data=f"generate_report_{scenario_id}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="🔄 Сгенерировать альтернативу",
                            callback_data=f"generate_alternative_{scenario['project_id']}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="⬅️ Назад к сценариям",
                            callback_data="back_to_scenarios"
                        )
                    ]
                ])
                
                await callback_query.message.edit_text(detail_text, reply_markup=keyboard)
            else:
                await callback_query.answer("❌ Ошибка получения данных сценария")
                
    except Exception as e:
        logger.error(f"Ошибка показа деталей сценария: {e}")
        await callback_query.answer("❌ Ошибка показа деталей сценария")

@dp.callback_query(lambda c: c.data == "generate_new_scenarios")
async def generate_new_scenarios(callback_query: types.CallbackQuery):
    try:
        async with httpx.AsyncClient() as client:
            # Получаем пользователя
            user_response = await client.get(f"{API_URL}/users/{callback_query.from_user.id}")
            if user_response.status_code == 200:
                user = user_response.json()
                user_id = user["id"]
                
                # Получаем проекты пользователя
                projects_response = await client.get(f"{API_URL}/projects/?user_id={user_id}")
                if projects_response.status_code == 200:
                    projects = projects_response.json()
                    
                    await callback_query.message.edit_text(
                        "🔄 Генерируем новые сценарии для всех проектов...",
                        reply_markup=None
                    )
                    
                    generated_count = 0
                    for project in projects:
                        # Генерируем сценарии
                        generate_response = await client.post(
                            f"{API_URL}/projects/{project['id']}/scenarios/generate",
                            params={"count": 3}
                        )
                        
                        if generate_response.status_code == 200:
                            generated_count += 1
                    
                    await callback_query.message.edit_text(
                        f"🎉 Сгенерированы новые сценарии для {generated_count} проектов!\n\nНажмите '📈 Сценарии' для просмотра.",
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="📈 Показать сценарии", callback_data="show_scenarios")]
                        ])
                    )
                else:
                    await callback_query.answer("❌ Ошибка получения проектов")
            else:
                await callback_query.answer("❌ Ошибка получения данных пользователя")
                
    except Exception as e:
        logger.error(f"Ошибка генерации новых сценариев: {e}")
        await callback_query.answer("❌ Ошибка генерации сценариев")

@dp.callback_query(lambda c: c.data == "back_to_scenarios")
async def back_to_scenarios(callback_query: types.CallbackQuery):
    try:
        # Вызываем функцию показа сценариев
        await show_scenarios(callback_query.message)
        await callback_query.answer()
    except Exception as e:
        logger.error(f"Ошибка возврата к сценариям: {e}")
        await callback_query.answer("❌ Ошибка возврата к сценариям")

@dp.callback_query(lambda c: c.data.startswith('generate_report_'))
async def generate_scenario_report(callback_query: types.CallbackQuery):
    try:
        scenario_id = int(callback_query.data.split('_')[2])
        
        await callback_query.message.edit_text(
            "📊 Генерируем PDF отчет...",
            reply_markup=None
        )
        
        async with httpx.AsyncClient() as client:
            # Генерируем отчет
            report_response = await client.post(f"{API_URL}/scenarios/{scenario_id}/report")
            
            if report_response.status_code == 200:
                report_data = report_response.json()
                report_url = report_data.get('report_url')
                
                if report_url:
                    await callback_query.message.edit_text(
                        f"📊 Отчет готов!\n\nСкачать: {report_url}",
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_scenarios")]
                        ])
                    )
                else:
                    await callback_query.message.edit_text(
                        "❌ Ошибка получения ссылки на отчет",
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_scenarios")]
                        ])
                    )
            else:
                await callback_query.message.edit_text(
                    "❌ Ошибка генерации отчета",
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_scenarios")]
                    ])
                )
                
    except Exception as e:
        logger.error(f"Ошибка генерации отчета: {e}")
        await callback_query.answer("❌ Ошибка генерации отчета")

@dp.callback_query(lambda c: c.data.startswith('generate_alternative_'))
async def generate_alternative_scenario(callback_query: types.CallbackQuery):
    try:
        project_id = int(callback_query.data.split('_')[2])
        
        await callback_query.message.edit_text(
            "🔄 Генерируем альтернативный сценарий...",
            reply_markup=None
        )
        
        async with httpx.AsyncClient() as client:
            # Генерируем альтернативный сценарий
            generate_response = await client.post(
                f"{API_URL}/projects/{project_id}/scenarios/generate",
                params={"count": 1}
            )
            
            if generate_response.status_code == 200:
                new_scenarios = generate_response.json()
                if new_scenarios:
                    new_scenario = new_scenarios[0]
                    await callback_query.message.edit_text(
                        f"🆕 Новый альтернативный сценарий:\n\n"
                        f"📊 {new_scenario['name']}\n"
                        f"💰 ROI: {new_scenario['roi']}%\n"
                        f"💵 Стоимость: {new_scenario['estimated_cost']:,.0f} ₽\n"
                        f"⏱️ Время: {new_scenario['construction_time']}\n"
                        f"⚠️ Риск: {new_scenario['risk_level']}",
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(
                                text="📊 Подробности",
                                callback_data=f"scenario_detail_{new_scenario['id']}"
                            )],
                            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_scenarios")]
                        ])
                    )
                else:
                    await callback_query.message.edit_text(
                        "❌ Не удалось сгенерировать альтернативный сценарий",
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_scenarios")]
                        ])
                    )
            else:
                await callback_query.message.edit_text(
                    "❌ Ошибка генерации альтернативного сценария",
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_scenarios")]
                    ])
                )
                
    except Exception as e:
        logger.error(f"Ошибка генерации альтернативного сценария: {e}")
        await callback_query.answer("❌ Ошибка генерации альтернативного сценария")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = """
📚 Справка по использованию бота:

🏗️ Создать проект - создание нового проекта недвижимости
📊 Мои проекты - просмотр ваших проектов
👷 Подрядчики - поиск и подбор подрядчиков
📈 Сценарии - генерация сценариев развития

Для начала работы создайте новый проект!
    """
    
    await message.answer(help_text, reply_markup=get_main_keyboard())

@dp.message(lambda message: message.text == "🏗️ Создать проект")
async def create_project_start(message: types.Message, state: FSMContext):
    await message.answer("Введите название проекта:", reply_markup=get_back_keyboard())
    await state.set_state(ProjectStates.waiting_for_name)

@dp.message(lambda message: message.text == "📊 Мои проекты")
async def show_projects(message: types.Message):
    try:
        async with httpx.AsyncClient() as client:
            # Сначала получаем пользователя по telegram_id
            user_response = await client.get(f"{API_URL}/users/{message.from_user.id}")
            if user_response.status_code == 404:
                # Создаем пользователя, если его нет
                user_data = {
                    "telegram_id": message.from_user.id,
                    "username": message.from_user.username,
                    "first_name": message.from_user.first_name,
                    "last_name": message.from_user.last_name
                }
                user_response = await client.post(f"{API_URL}/users", json=user_data)
            
            if user_response.status_code == 200:
                user = user_response.json()
                user_id = user["id"]
                
                # Получаем проекты пользователя
                response = await client.get(f"{API_URL}/projects/?user_id={user_id}")
                if response.status_code == 200:
                    projects = response.json()
                    if projects:
                        projects_text = "📊 Ваши проекты:\n\n"
                        for project in projects:
                            projects_text += f"🏗️ {project['name']}\n"
                            projects_text += f"📍 {project['location'] or 'Не указано'}\n"
                            projects_text += f"💰 Бюджет: {project['budget'] or 'Не указан'}\n"
                            projects_text += f"📅 Создан: {project['created_at'][:10]}\n\n"
                    else:
                        projects_text = "У вас пока нет проектов. Создайте первый!"
                else:
                    projects_text = "Ошибка получения проектов"
            else:
                projects_text = "Ошибка получения данных пользователя"
    except Exception as e:
        logger.error(f"Ошибка получения проектов: {e}")
        projects_text = "Ошибка получения проектов"
    
    await message.answer(projects_text, reply_markup=get_main_keyboard())

@dp.message(lambda message: message.text == "👷 Подрядчики")
async def show_contractors(message: types.Message):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/contractors/")
            if response.status_code == 200:
                contractors = response.json()
                if contractors:
                    # Дедупликация по ID подрядчика
                    unique_contractors = {}
                    for contractor in contractors:
                        contractor_id = contractor.get('id')
                        if contractor_id and contractor_id not in unique_contractors:
                            unique_contractors[contractor_id] = contractor
                    
                    # Берем только уникальных подрядчиков (максимум 5)
                    unique_contractors_list = list(unique_contractors.values())[:5]
                    
                    contractors_text = "👷 Доступные подрядчики:\n\n"
                    for contractor in unique_contractors_list:
                        contractors_text += f"🏢 {contractor['name']}\n"
                        contractors_text += f"🎯 {contractor['specialization']}\n"
                        contractors_text += f"⭐ Рейтинг: {contractor['rating'] or 'Нет'}\n"
                        contractors_text += f"📞 {contractor.get('contact_phone', 'Не указан')}\n\n"
                else:
                    contractors_text = "Подрядчики не найдены"
            else:
                contractors_text = "Ошибка получения подрядчиков"
    except Exception as e:
        logger.error(f"Ошибка получения подрядчиков: {e}")
        contractors_text = "Ошибка получения подрядчиков"
    
    await message.answer(contractors_text, reply_markup=get_main_keyboard())

@dp.message(lambda message: message.text == "📈 Сценарии")
async def show_scenarios(message: types.Message):
    try:
        async with httpx.AsyncClient() as client:
            # Сначала получаем пользователя по telegram_id
            user_response = await client.get(f"{API_URL}/users/{message.from_user.id}")
            if user_response.status_code == 404:
                # Создаем пользователя, если его нет
                user_data = {
                    "telegram_id": message.from_user.id,
                    "username": message.from_user.username,
                    "first_name": message.from_user.first_name,
                    "last_name": message.from_user.last_name
                }
                user_response = await client.post(f"{API_URL}/users", json=user_data)
            
            if user_response.status_code == 200:
                user = user_response.json()
                user_id = user["id"]
                
                # Получаем проекты пользователя
                projects_response = await client.get(f"{API_URL}/projects/?user_id={user_id}")
                if projects_response.status_code == 200:
                    projects = projects_response.json()
                    
                    if not projects:
                        await message.answer(
                            "📈 У вас пока нет проектов. Создайте первый проект для генерации сценариев!",
                            reply_markup=get_main_keyboard()
                        )
                        return
                    
                    # Собираем все сценарии для всех проектов пользователя
                    all_scenarios = []
                    scenarios_text = "📈 Ваши сценарии развития:\n\n"
                    
                    for project in projects:
                        project_scenarios_response = await client.get(f"{API_URL}/projects/{project['id']}/scenarios/")
                        if project_scenarios_response.status_code == 200:
                            project_scenarios = project_scenarios_response.json()
                            
                            if project_scenarios:
                                scenarios_text += f"🏗️ Проект: {project['name']}\n"
                                scenarios_text += f"📍 {project['location'] or 'Не указано'}\n\n"
                                
                                for scenario in project_scenarios:
                                    scenarios_text += f"📊 {scenario['name']}\n"
                                    scenarios_text += f"💰 ROI: {scenario['roi']}%\n"
                                    scenarios_text += f"💵 Стоимость: {scenario['estimated_cost']:,.0f} ₽\n"
                                    scenarios_text += f"⏱️ Время: {scenario['construction_time']}\n"
                                    scenarios_text += f"⚠️ Риск: {scenario['risk_level']}\n\n"
                                
                                scenarios_text += "─" * 30 + "\n\n"
                                all_scenarios.extend(project_scenarios)
                    
                    if all_scenarios:
                        # Создаем интерактивную клавиатуру для выбора сценариев
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
                        
                        for scenario in all_scenarios:
                            keyboard.inline_keyboard.append([
                                InlineKeyboardButton(
                                    text=f"📊 {scenario['name']} (ROI: {scenario['roi']}%)",
                                    callback_data=f"scenario_detail_{scenario['id']}"
                                )
                            ])
                        
                        # Добавляем кнопку для генерации новых сценариев
                        keyboard.inline_keyboard.append([
                            InlineKeyboardButton(
                                text="🔄 Сгенерировать новые сценарии",
                                callback_data="generate_new_scenarios"
                            )
                        ])
                        
                        await message.answer(scenarios_text, reply_markup=keyboard)
                    else:
                        # Если сценариев нет, генерируем их для всех проектов
                        await message.answer(
                            "📈 Генерируем сценарии для всех ваших проектов...",
                            reply_markup=get_main_keyboard()
                        )
                        
                        for project in projects:
                            # Генерируем сценарии
                            generate_response = await client.post(
                                f"{API_URL}/projects/{project['id']}/scenarios/generate",
                                params={"count": 3}
                            )
                            
                            if generate_response.status_code == 200:
                                await message.answer(
                                    f"✅ Сценарии для проекта '{project['name']}' сгенерированы!",
                                    reply_markup=get_main_keyboard()
                                )
                        
                        await message.answer(
                            "🎉 Все сценарии сгенерированы! Нажмите '📈 Сценарии' еще раз для просмотра.",
                            reply_markup=get_main_keyboard()
                        )
                else:
                    await message.answer(
                        "❌ Ошибка получения проектов",
                        reply_markup=get_main_keyboard()
                    )
            else:
                await message.answer(
                    "❌ Ошибка получения данных пользователя",
                    reply_markup=get_main_keyboard()
                )
    except Exception as e:
        logger.error(f"Ошибка получения сценариев: {e}")
        await message.answer(
            "❌ Ошибка получения сценариев",
            reply_markup=get_main_keyboard()
        )

@dp.message(lambda message: message.text == "ℹ️ Помощь")
async def show_help(message: types.Message):
    await cmd_help(message)

@dp.message(lambda message: message.text == "🔙 Назад")
async def go_back(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Главное меню:", reply_markup=get_main_keyboard())

@dp.message(ProjectStates.waiting_for_name)
async def process_project_name(message: types.Message, state: FSMContext):
    if message.text == "🔙 Назад":
        await go_back(message, state)
        return
    
    await state.update_data(project_name=message.text)
    await message.answer("Выберите тип проекта:", reply_markup=get_project_type_keyboard())
    await state.set_state(ProjectStates.waiting_for_type)

@dp.message(ProjectStates.waiting_for_type)
async def process_project_type(message: types.Message, state: FSMContext):
    if message.text == "🔙 Назад":
        await message.answer("Введите название проекта:", reply_markup=get_back_keyboard())
        await state.set_state(ProjectStates.waiting_for_name)
        return
    
    type_mapping = {
        "🏠 Жилой": "residential",
        "🏢 Коммерческий": "commercial", 
        "🏭 Промышленный": "industrial",
        "🏘️ Смешанный": "mixed"
    }
    
    if message.text in type_mapping:
        await state.update_data(project_type=type_mapping[message.text])
        await message.answer("Введите локацию проекта:", reply_markup=get_back_keyboard())
        await state.set_state(ProjectStates.waiting_for_location)
    else:
        await message.answer("Пожалуйста, выберите тип проекта из списка:")

@dp.message(ProjectStates.waiting_for_location)
async def process_project_location(message: types.Message, state: FSMContext):
    if message.text == "🔙 Назад":
        await message.answer("Выберите тип проекта:", reply_markup=get_project_type_keyboard())
        await state.set_state(ProjectStates.waiting_for_type)
        return
    
    await state.update_data(location=message.text)
    await message.answer("Введите бюджет проекта (в рублях):", reply_markup=get_back_keyboard())
    await state.set_state(ProjectStates.waiting_for_budget)

@dp.message(ProjectStates.waiting_for_budget)
async def process_project_budget(message: types.Message, state: FSMContext):
    if message.text == "🔙 Назад":
        await message.answer("Введите локацию проекта:", reply_markup=get_back_keyboard())
        await state.set_state(ProjectStates.waiting_for_location)
        return
    
    try:
        budget = float(message.text.replace(" ", "").replace(",", ""))
        await state.update_data(budget=budget)
        await message.answer("Введите площадь проекта (в кв.м):", reply_markup=get_back_keyboard())
        await state.set_state(ProjectStates.waiting_for_area)
    except ValueError:
        await message.answer("Пожалуйста, введите корректную сумму (например: 1000000):")

@dp.message(ProjectStates.waiting_for_area)
async def process_project_area(message: types.Message, state: FSMContext):
    if message.text == "🔙 Назад":
        await message.answer("Введите бюджет проекта:", reply_markup=get_back_keyboard())
        await state.set_state(ProjectStates.waiting_for_budget)
        return
    
    try:
        area = float(message.text.replace(" ", "").replace(",", ""))
        await state.update_data(area=area)
        
        # Получаем все данные проекта
        project_data = await state.get_data()
        
        # Создаем проект через API
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_URL}/projects/",
                    json={
                        "name": project_data["project_name"],
                        "project_type": project_data["project_type"],
                        "location": project_data["location"],
                        "budget": project_data["budget"],
                        "area": area,
                        "user_id": message.from_user.id
                    }
                )
                
                if response.status_code == 200:
                    project = response.json()
                    
                    # Генерируем сценарии
                    scenarios_response = await client.post(
                        f"{API_URL}/projects/{project['id']}/scenarios/generate",
                        params={"count": 3}
                    )
                    
                    success_text = f"""
✅ Проект "{project_data['project_name']}" успешно создан!

📊 Информация о проекте:
• Тип: {project_data['project_type']}
• Локация: {project_data['location']}
• Бюджет: {project_data['budget']:,} ₽
• Площадь: {area} кв.м

🎯 Сценарии развития сгенерированы!
                    """
                    
                    await message.answer(success_text, reply_markup=get_main_keyboard())
                    await state.clear()
                    
                else:
                    await message.answer(
                        "❌ Ошибка создания проекта. Попробуйте позже.",
                        reply_markup=get_main_keyboard()
                    )
                    await state.clear()
                    
        except Exception as e:
            logger.error(f"Ошибка создания проекта: {e}")
            await message.answer(
                "❌ Ошибка создания проекта. Попробуйте позже.",
                reply_markup=get_main_keyboard()
            )
            await state.clear()
            
    except ValueError:
        await message.answer("Пожалуйста, введите корректную площадь (например: 1000):")

# Обработчик неизвестных сообщений
@dp.message()
async def echo_message(message: types.Message):
    await message.answer(
        "Пожалуйста, используйте кнопки меню для навигации.",
        reply_markup=get_main_keyboard()
    )

async def main():
    """Главная функция запуска бота"""
    print("🤖 Запуск TrendPulse AI бота v2.0.0...")
    print(f"🔗 API URL: {API_URL}")
    
    # Проверяем подключение к API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/health")
            if response.status_code == 200:
                print("✅ API доступен")
                
                # Получаем информацию о версии API
                api_info_response = await client.get(f"{API_URL}/api-info")
                if api_info_response.status_code == 200:
                    api_info = api_info_response.json()
                    print(f"📊 API версия: {api_info['version']}")
                    print(f"🎯 Возможности: {len(api_info['capabilities'])} функций")
            else:
                print("⚠️ API недоступен")
    except Exception as e:
        print(f"⚠️ Не удалось подключиться к API: {e}")
    
    print("🚀 Бот готов к работе!")
    print("💡 Отправьте /start в Telegram для начала работы")
    
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 
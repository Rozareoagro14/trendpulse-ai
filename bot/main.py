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
            [KeyboardButton(text="🏭 Смешанный")],
            [KeyboardButton(text="🏭 Промышленный")],
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

@dp.callback_query(lambda c: c.data.startswith("scenario_detail_"))
async def process_scenario_detail(callback: types.CallbackQuery):
    """Детальный просмотр сценария"""
    await callback.answer("Функция в разработке")

@dp.callback_query(lambda c: c.data == "generate_pdf")
async def process_generate_pdf(callback: types.CallbackQuery):
    """Генерация PDF отчета"""
    await callback.answer("Функция в разработке")

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
            response = await client.get(f"{API_URL}/projects/")
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
                    contractors_text = "👷 Доступные подрядчики:\n\n"
                    for contractor in contractors[:5]:  # Показываем первые 5
                        contractors_text += f"🏢 {contractor['name']}\n"
                        contractors_text += f"🎯 {contractor['specialization']}\n"
                        contractors_text += f"⭐ Рейтинг: {contractor['rating'] or 'Нет'}\n"
                        contractors_text += f"📞 {contractor['contact_phone'] or 'Не указан'}\n\n"
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
    await message.answer(
        "📈 Для генерации сценариев сначала создайте проект!",
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
        "🏭 Смешанный": "mixed",
        "🏭 Промышленный": "industrial"
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
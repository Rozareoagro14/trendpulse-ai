from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton
from .models import ZoneType, InfrastructureType, ProjectType

class KeyboardFactory:
    """Фабрика для создания клавиатур"""
    
    @staticmethod
    def get_main_keyboard():
        """Главная клавиатура"""
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="🏗️ Создать сценарий",
            callback_data="create_scenario"
        ))
        builder.add(InlineKeyboardButton(
            text="📊 Мои сценарии",
            callback_data="my_scenarios"
        ))
        builder.add(InlineKeyboardButton(
            text="👷 Подрядчики",
            callback_data="get_contractors"
        ))
        builder.add(InlineKeyboardButton(
            text="📄 Отчеты",
            callback_data="reports"
        ))
        builder.add(InlineKeyboardButton(
            text="👤 Профиль",
            callback_data="profile"
        ))
        builder.add(InlineKeyboardButton(
            text="ℹ️ О проекте",
            callback_data="about_project"
        ))
        builder.adjust(2)  # 2 кнопки в ряд
        return builder.as_markup()
    
    @staticmethod
    def get_zone_keyboard():
        """Клавиатура выбора зонирования"""
        builder = InlineKeyboardBuilder()
        zones = [
            ("🏠 Жилая", ZoneType.RESIDENTIAL),
            ("🏢 Коммерческая", ZoneType.COMMERCIAL),
            ("🏭 Промышленная", ZoneType.INDUSTRIAL),
            ("🌾 Сельхоз", ZoneType.AGRICULTURAL),
            ("🏘️ Смешанная", ZoneType.MIXED)
        ]
        
        for name, zone in zones:
            builder.add(InlineKeyboardButton(
                text=name,
                callback_data=f"zone_{zone.value}"
            ))
        
        builder.add(InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="back_to_main"
        ))
        
        builder.adjust(2)  # 2 кнопки в ряд
        return builder.as_markup()
    
    @staticmethod
    def get_infrastructure_keyboard():
        """Клавиатура выбора инфраструктуры"""
        builder = InlineKeyboardBuilder()
        infrastructure = [
            ("⚡ Электричество", InfrastructureType.ELECTRICITY),
            ("🔥 Газ", InfrastructureType.GAS),
            ("💧 Вода", InfrastructureType.WATER),
            ("🚰 Канализация", InfrastructureType.SEWERAGE),
            ("🛣️ Дороги", InfrastructureType.ROAD),
            ("🌐 Интернет", InfrastructureType.INTERNET)
        ]
        
        for name, infra in infrastructure:
            builder.add(InlineKeyboardButton(
                text=name,
                callback_data=f"infra_{infra.value}"
            ))
        
        builder.add(InlineKeyboardButton(
            text="✅ Готово",
            callback_data="infrastructure_done"
        ))
        builder.add(InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="back_to_zone"
        ))
        
        builder.adjust(2)
        return builder.as_markup()
    
    @staticmethod
    def get_scenario_actions_keyboard(scenario_id: int):
        """Клавиатура действий со сценарием"""
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="📄 Создать PDF",
            callback_data=f"generate_pdf_{scenario_id}"
        ))
        builder.add(InlineKeyboardButton(
            text="👷 Подрядчики",
            callback_data=f"scenario_contractors_{scenario_id}"
        ))
        builder.add(InlineKeyboardButton(
            text="📊 Детали",
            callback_data=f"scenario_detail_{scenario_id}"
        ))
        builder.add(InlineKeyboardButton(
            text="🔄 Новый сценарий",
            callback_data="create_scenario"
        ))
        builder.add(InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="my_scenarios"
        ))
        builder.adjust(2)
        return builder.as_markup()
    
    @staticmethod
    def get_pdf_type_keyboard(scenario_id: int):
        """Клавиатура выбора типа PDF отчета"""
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="📋 Пред-ТЭО",
            callback_data=f"pdf_pre_feasibility_{scenario_id}"
        ))
        builder.add(InlineKeyboardButton(
            text="📊 Инвестиционный меморандум",
            callback_data=f"pdf_investment_memo_{scenario_id}"
        ))
        builder.add(InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=f"scenario_actions_{scenario_id}"
        ))
        builder.adjust(1)
        return builder.as_markup()
    
    @staticmethod
    def get_contractor_filter_keyboard():
        """Клавиатура фильтрации подрядчиков"""
        builder = InlineKeyboardBuilder()
        project_types = [
            ("🏠 Жилое", ProjectType.RESIDENTIAL_COMPLEX),
            ("🏢 Коммерческое", ProjectType.COMMERCIAL),
            ("🏭 Промышленное", ProjectType.INDUSTRIAL_PARK),
            ("🌾 Сельхоз", ProjectType.AGRICULTURAL_PROCESSING),
            ("📦 Логистика", ProjectType.LOGISTICS_CENTER),
            ("💻 Дата-центр", ProjectType.DATA_CENTER)
        ]
        
        for name, pt in project_types:
            builder.add(InlineKeyboardButton(
                text=name,
                callback_data=f"filter_contractor_{pt.value}"
            ))
        
        builder.add(InlineKeyboardButton(
            text="👥 Все подрядчики",
            callback_data="all_contractors"
        ))
        builder.add(InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="back_to_main"
        ))
        builder.adjust(2)
        return builder.as_markup()
    
    @staticmethod
    def get_profile_keyboard():
        """Клавиатура профиля пользователя"""
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="✏️ Изменить имя",
            callback_data="edit_name"
        ))
        builder.add(InlineKeyboardButton(
            text="📞 Изменить телефон",
            callback_data="edit_phone"
        ))
        builder.add(InlineKeyboardButton(
            text="👤 Изменить роль",
            callback_data="edit_role"
        ))
        builder.add(InlineKeyboardButton(
            text="📊 Моя статистика",
            callback_data="my_stats"
        ))
        builder.add(InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="back_to_main"
        ))
        builder.adjust(2)
        return builder.as_markup()
    
    @staticmethod
    def get_role_keyboard():
        """Клавиатура выбора роли"""
        builder = InlineKeyboardBuilder()
        roles = [
            ("💰 Инвестор", "investor"),
            ("🏗️ Девелопер", "developer"),
            ("👷 Подрядчик", "contractor")
        ]
        
        for name, role in roles:
            builder.add(InlineKeyboardButton(
                text=name,
                callback_data=f"role_{role}"
            ))
        
        builder.add(InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="profile"
        ))
        builder.adjust(1)
        return builder.as_markup()
    
    @staticmethod
    def get_yes_no_keyboard(callback_data_yes: str, callback_data_no: str):
        """Клавиатура Да/Нет"""
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="✅ Да",
            callback_data=callback_data_yes
        ))
        builder.add(InlineKeyboardButton(
            text="❌ Нет",
            callback_data=callback_data_no
        ))
        return builder.as_markup()
    
    @staticmethod
    def get_back_keyboard(callback_data: str):
        """Простая клавиатура с кнопкой назад"""
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=callback_data
        ))
        return builder.as_markup()
    
    @staticmethod
    def get_cancel_keyboard():
        """Клавиатура отмены"""
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="❌ Отмена",
            callback_data="cancel"
        ))
        return builder.as_markup()

class ReplyKeyboardFactory:
    """Фабрика для создания reply клавиатур"""
    
    @staticmethod
    def get_main_reply_keyboard():
        """Главная reply клавиатура"""
        builder = ReplyKeyboardBuilder()
        builder.add(KeyboardButton(text="🏗️ Создать сценарий"))
        builder.add(KeyboardButton(text="📊 Мои сценарии"))
        builder.add(KeyboardButton(text="👷 Подрядчики"))
        builder.add(KeyboardButton(text="👤 Профиль"))
        builder.add(KeyboardButton(text="ℹ️ Помощь"))
        builder.adjust(2)
        return builder.as_markup(resize_keyboard=True)
    
    @staticmethod
    def get_contact_keyboard():
        """Клавиатура для отправки контакта"""
        builder = ReplyKeyboardBuilder()
        builder.add(KeyboardButton(
            text="📞 Отправить контакт",
            request_contact=True
        ))
        builder.add(KeyboardButton(text="❌ Отмена"))
        return builder.as_markup(resize_keyboard=True, one_time_keyboard=True) 
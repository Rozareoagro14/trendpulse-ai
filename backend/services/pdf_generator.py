import os
import tempfile
from datetime import datetime
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

class PDFGenerator:
    """Сервис для генерации PDF отчетов"""
    
    def __init__(self):
        # Настройка Jinja2
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
        # Создаем директорию для шаблонов если её нет
        os.makedirs(template_dir, exist_ok=True)
        
        # Создаем базовый шаблон если его нет
        self._create_base_template()
    
    def _create_base_template(self):
        """Создает базовый HTML шаблон для отчетов"""
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'base.html')
        
        if not os.path.exists(template_path):
            base_template = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 20px;
        }
        .header {
            text-align: center;
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #2c3e50;
            margin: 0;
            font-size: 28px;
        }
        .header .subtitle {
            color: #7f8c8d;
            font-size: 16px;
            margin-top: 10px;
        }
        .section {
            margin-bottom: 30px;
        }
        .section h2 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        .info-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }
        .info-item h3 {
            margin: 0 0 10px 0;
            color: #2c3e50;
            font-size: 16px;
        }
        .info-item p {
            margin: 0;
            font-size: 18px;
            font-weight: bold;
            color: #27ae60;
        }
        .table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        .table th, .table td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        .table th {
            background-color: #2c3e50;
            color: white;
        }
        .table tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .highlight {
            background-color: #e8f5e8;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #27ae60;
            margin: 20px 0;
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
        }
        .roi-high {
            color: #27ae60;
            font-weight: bold;
        }
        .roi-medium {
            color: #f39c12;
            font-weight: bold;
        }
        .roi-low {
            color: #e74c3c;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ title }}</h1>
        <div class="subtitle">{{ subtitle }}</div>
    </div>
    
    {% block content %}{% endblock %}
    
    <div class="footer">
        <p>Отчет сгенерирован системой TrendPulse AI</p>
        <p>{{ generated_at }}</p>
    </div>
</body>
</html>
            """
            
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(base_template)
    
    def generate_pre_feasibility_report(self, scenario_data: Dict[str, Any], 
                                      land_plot_data: Dict[str, Any],
                                      user_data: Dict[str, Any]) -> str:
        """Генерирует пред-ТЭО в формате PDF"""
        
        # Подготавливаем данные для шаблона
        template_data = {
            'title': f'Пред-ТЭО: {scenario_data["name"]}',
            'subtitle': f'Участок {land_plot_data["area"]} га, {land_plot_data["zone_type"]}',
            'generated_at': datetime.now().strftime('%d.%m.%Y %H:%M'),
            'scenario': scenario_data,
            'land_plot': land_plot_data,
            'user': user_data
        }
        
        # Рендерим HTML
        template = self.env.get_template('pre_feasibility.html')
        html_content = template.render(**template_data)
        
        # Создаем временный файл для PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            pdf_path = tmp_file.name
        
        # Генерируем PDF
        font_config = FontConfiguration()
        HTML(string=html_content).write_pdf(
            pdf_path,
            font_config=font_config
        )
        
        return pdf_path
    
    def generate_investment_memo(self, scenario_data: Dict[str, Any],
                               land_plot_data: Dict[str, Any],
                               user_data: Dict[str, Any]) -> str:
        """Генерирует инвестиционный меморандум"""
        
        template_data = {
            'title': f'Инвестиционный меморандум: {scenario_data["name"]}',
            'subtitle': f'Детальный анализ инвестиционного проекта',
            'generated_at': datetime.now().strftime('%d.%m.%Y %H:%M'),
            'scenario': scenario_data,
            'land_plot': land_plot_data,
            'user': user_data
        }
        
        template = self.env.get_template('investment_memo.html')
        html_content = template.render(**template_data)
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            pdf_path = tmp_file.name
        
        font_config = FontConfiguration()
        HTML(string=html_content).write_pdf(
            pdf_path,
            font_config=font_config
        )
        
        return pdf_path
    
    def _get_roi_class(self, roi: float) -> str:
        """Возвращает CSS класс для ROI в зависимости от значения"""
        if roi >= 20:
            return 'roi-high'
        elif roi >= 10:
            return 'roi-medium'
        else:
            return 'roi-low'
    
    def create_pre_feasibility_template(self):
        """Создает шаблон пред-ТЭО"""
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'pre_feasibility.html')
        
        if not os.path.exists(template_path):
            template_content = """
{% extends "base.html" %}

{% block content %}
<div class="section">
    <h2>1. Резюме проекта</h2>
    <div class="info-grid">
        <div class="info-item">
            <h3>Название проекта</h3>
            <p>{{ scenario.name }}</p>
        </div>
        <div class="info-item">
            <h3>Тип проекта</h3>
            <p>{{ scenario.project_type }}</p>
        </div>
        <div class="info-item">
            <h3>Площадь участка</h3>
            <p>{{ land_plot.area }} га</p>
        </div>
        <div class="info-item">
            <h3>Зонирование</h3>
            <p>{{ land_plot.zone_type }}</p>
        </div>
    </div>
    
    <div class="highlight">
        <h3>Ключевые показатели эффективности</h3>
        <div class="info-grid">
            <div class="info-item">
                <h3>ROI</h3>
                <p class="{{ roi_class }}">{{ "%.1f"|format(scenario.unit_economics.roi_percentage) }}%</p>
            </div>
            <div class="info-item">
                <h3>Общие инвестиции</h3>
                <p>{{ "{:,.0f}".format(scenario.unit_economics.total_investment) }} ₽</p>
            </div>
            <div class="info-item">
                <h3>Срок окупаемости</h3>
                <p>{{ "%.1f"|format(scenario.unit_economics.payback_period) }} лет</p>
            </div>
            <div class="info-item">
                <h3>Срок строительства</h3>
                <p>{{ scenario.construction_time }}</p>
            </div>
        </div>
    </div>
</div>

<div class="section">
    <h2>2. Характеристики участка</h2>
    <table class="table">
        <tr>
            <th>Параметр</th>
            <th>Значение</th>
        </tr>
        <tr>
            <td>Площадь</td>
            <td>{{ land_plot.area }} га</td>
        </tr>
        <tr>
            <td>Тип зонирования</td>
            <td>{{ land_plot.zone_type }}</td>
        </tr>
        <tr>
            <td>Инфраструктура</td>
            <td>{{ land_plot.infrastructure | join(', ') }}</td>
        </tr>
        <tr>
            <td>Электричество</td>
            <td>{% if land_plot.electricity_power %}{{ land_plot.electricity_power }} МВт{% else %}Не подключено{% endif %}</td>
        </tr>
        <tr>
            <td>Дорожный доступ</td>
            <td>{% if land_plot.road_access %}Есть{% else %}Нет{% endif %}</td>
        </tr>
        <tr>
            <td>Интернет</td>
            <td>{% if land_plot.internet_available %}Доступен{% else %}Недоступен{% endif %}</td>
        </tr>
    </table>
</div>

<div class="section">
    <h2>3. Финансовая модель</h2>
    <table class="table">
        <tr>
            <th>Показатель</th>
            <th>Значение</th>
        </tr>
        <tr>
            <td>Общие инвестиции</td>
            <td>{{ "{:,.0f}".format(scenario.unit_economics.total_investment) }} ₽</td>
        </tr>
        <tr>
            <td>Стоимость строительства</td>
            <td>{{ "{:,.0f}".format(scenario.unit_economics.construction_cost) }} ₽</td>
        </tr>
        <tr>
            <td>Стоимость инфраструктуры</td>
            <td>{{ "{:,.0f}".format(scenario.unit_economics.infrastructure_cost) }} ₽</td>
        </tr>
        <tr>
            <td>Операционные расходы (год)</td>
            <td>{{ "{:,.0f}".format(scenario.unit_economics.operational_cost) }} ₽</td>
        </tr>
        <tr>
            <td>Доход в год</td>
            <td>{{ "{:,.0f}".format(scenario.unit_economics.revenue_per_year) }} ₽</td>
        </tr>
        <tr>
            <td>ROI</td>
            <td class="{{ roi_class }}">{{ "%.1f"|format(scenario.unit_economics.roi_percentage) }}%</td>
        </tr>
        <tr>
            <td>Срок окупаемости</td>
            <td>{{ "%.1f"|format(scenario.unit_economics.payback_period) }} лет</td>
        </tr>
        <tr>
            <td>NPV</td>
            <td>{{ "{:,.0f}".format(scenario.unit_economics.npv) }} ₽</td>
        </tr>
        <tr>
            <td>IRR</td>
            <td>{{ "%.1f"|format(scenario.unit_economics.irr) }}%</td>
        </tr>
    </table>
</div>

<div class="section">
    <h2>4. Анализ рисков</h2>
    <div class="info-grid">
        <div class="info-item">
            <h3>Уровень риска</h3>
            <p>{{ scenario.risk_level }}</p>
        </div>
        <div class="info-item">
            <h3>Рыночный спрос</h3>
            <p>{{ scenario.market_demand }}</p>
        </div>
        <div class="info-item">
            <h3>Регуляторная сложность</h3>
            <p>{{ scenario.regulatory_complexity }}</p>
        </div>
    </div>
</div>

{% if scenario.recommendations %}
<div class="section">
    <h2>5. Рекомендации</h2>
    <ul>
        {% for recommendation in scenario.recommendations %}
        <li>{{ recommendation }}</li>
        {% endfor %}
    </ul>
</div>
{% endif %}

<div class="section">
    <h2>6. Описание проекта</h2>
    <p>{{ scenario.description }}</p>
</div>
{% endblock %}
            """
            
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(template_content)
    
    def create_investment_memo_template(self):
        """Создает шаблон инвестиционного меморандума"""
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'investment_memo.html')
        
        if not os.path.exists(template_path):
            template_content = """
{% extends "base.html" %}

{% block content %}
<div class="section">
    <h2>1. Исполнительное резюме</h2>
    <p>Данный инвестиционный меморандум представляет детальный анализ проекта {{ scenario.name }} 
    на участке площадью {{ land_plot.area }} га в зоне {{ land_plot.zone_type }}.</p>
    
    <div class="highlight">
        <h3>Ключевые инвестиционные показатели</h3>
        <div class="info-grid">
            <div class="info-item">
                <h3>ROI</h3>
                <p class="{{ roi_class }}">{{ "%.1f"|format(scenario.unit_economics.roi_percentage) }}%</p>
            </div>
            <div class="info-item">
                <h3>Общие инвестиции</h3>
                <p>{{ "{:,.0f}".format(scenario.unit_economics.total_investment) }} ₽</p>
            </div>
            <div class="info-item">
                <h3>NPV</h3>
                <p>{{ "{:,.0f}".format(scenario.unit_economics.npv) }} ₽</p>
            </div>
            <div class="info-item">
                <h3>IRR</h3>
                <p>{{ "%.1f"|format(scenario.unit_economics.irr) }}%</p>
            </div>
        </div>
    </div>
</div>

<div class="section">
    <h2>2. Анализ рынка</h2>
    <p>Рыночный спрос: <strong>{{ scenario.market_demand }}</strong></p>
    <p>Регуляторная среда: <strong>{{ scenario.regulatory_complexity }}</strong></p>
</div>

<div class="section">
    <h2>3. Детальная финансовая модель</h2>
    <table class="table">
        <tr>
            <th>Показатель</th>
            <th>Значение</th>
            <th>Комментарий</th>
        </tr>
        <tr>
            <td>Общие инвестиции</td>
            <td>{{ "{:,.0f}".format(scenario.unit_economics.total_investment) }} ₽</td>
            <td>Включает строительство и инфраструктуру</td>
        </tr>
        <tr>
            <td>Стоимость строительства</td>
            <td>{{ "{:,.0f}".format(scenario.unit_economics.construction_cost) }} ₽</td>
            <td>{{ "{:,.0f}".format(scenario.unit_economics.construction_cost / land_plot.area) }} ₽/га</td>
        </tr>
        <tr>
            <td>Годовой доход</td>
            <td>{{ "{:,.0f}".format(scenario.unit_economics.revenue_per_year) }} ₽</td>
            <td>Прогноз на основе рыночных данных</td>
        </tr>
        <tr>
            <td>Операционные расходы</td>
            <td>{{ "{:,.0f}".format(scenario.unit_economics.operational_cost) }} ₽</td>
            <td>5% от общих инвестиций</td>
        </tr>
    </table>
</div>

<div class="section">
    <h2>4. Анализ чувствительности</h2>
    <p>Проект демонстрирует устойчивость к изменениям ключевых параметров:</p>
    <ul>
        <li>При снижении доходов на 10% ROI составит {{ "%.1f"|format(scenario.unit_economics.roi_percentage * 0.9) }}%</li>
        <li>При росте затрат на 10% ROI составит {{ "%.1f"|format(scenario.unit_economics.roi_percentage * 0.8) }}%</li>
        <li>Срок окупаемости остается в приемлемых пределах</li>
    </ul>
</div>

<div class="section">
    <h2>5. Рекомендации</h2>
    {% if scenario.recommendations %}
    <ul>
        {% for recommendation in scenario.recommendations %}
        <li>{{ recommendation }}</li>
        {% endfor %}
    </ul>
    {% else %}
    <p>Дополнительных рекомендаций не требуется.</p>
    {% endif %}
</div>
{% endblock %}
            """
            
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(template_content) 
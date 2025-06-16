#!/usr/bin/env python3
"""
Скрипт для добавления тестовых подрядчиков в базу данных
"""

import asyncio
import httpx
import json

# Конфигурация
API_URL = "http://localhost:8000"

# Данные подрядчиков
contractors_data = [
    {
        "name": "ООО СтройИнвест",
        "specialization": "Жилое строительство",
        "rating": 4.8,
        "contact_phone": "+7 (495) 123-45-67",
        "contact_email": "info@stroinvest.ru",
        "experience_years": 15,
        "completed_projects": 50
    },
    {
        "name": "ООО КоммерцСтрой",
        "specialization": "Коммерческое строительство",
        "rating": 4.6,
        "contact_phone": "+7 (495) 234-56-78",
        "contact_email": "contact@commercstroy.ru",
        "experience_years": 12,
        "completed_projects": 35
    },
    {
        "name": "ООО ПромСтрой",
        "specialization": "Промышленное строительство",
        "rating": 4.4,
        "contact_phone": "+7 (495) 345-67-89",
        "contact_email": "info@promstroy.ru",
        "experience_years": 18,
        "completed_projects": 25
    },
    {
        "name": "ООО ЭлитСтрой",
        "specialization": "Элитное жилье",
        "rating": 4.9,
        "contact_phone": "+7 (495) 456-78-90",
        "contact_email": "elite@elitstroy.ru",
        "experience_years": 20,
        "completed_projects": 15
    },
    {
        "name": "ООО БыстрыйСтрой",
        "specialization": "Быстровозводимые здания",
        "rating": 4.2,
        "contact_phone": "+7 (495) 567-89-01",
        "contact_email": "fast@faststroy.ru",
        "experience_years": 8,
        "completed_projects": 30
    }
]

async def add_contractors():
    """Добавляет подрядчиков в базу данных"""
    print("🏗️ Добавление подрядчиков в базу данных...")
    
    async with httpx.AsyncClient() as client:
        # Проверяем доступность API
        try:
            response = await client.get(f"{API_URL}/health")
            if response.status_code != 200:
                print(f"❌ API недоступен: {response.status_code}")
                return
            print("✅ API доступен")
        except Exception as e:
            print(f"❌ Ошибка подключения к API: {e}")
            return
        
        # Добавляем каждого подрядчика
        for i, contractor_data in enumerate(contractors_data, 1):
            try:
                print(f"📝 Добавление подрядчика {i}/{len(contractors_data)}: {contractor_data['name']}")
                
                response = await client.post(
                    f"{API_URL}/contractors/",
                    json=contractor_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    contractor = response.json()
                    print(f"✅ Подрядчик добавлен: ID {contractor['id']}")
                else:
                    print(f"❌ Ошибка добавления: {response.status_code} - {response.text}")
                    
            except Exception as e:
                print(f"❌ Ошибка при добавлении подрядчика {contractor_data['name']}: {e}")
        
        # Проверяем результат
        print("\n📊 Проверка результата...")
        try:
            response = await client.get(f"{API_URL}/contractors/")
            if response.status_code == 200:
                contractors = response.json()
                print(f"✅ Всего подрядчиков в базе: {len(contractors)}")
                
                for contractor in contractors:
                    print(f"  - {contractor['name']} (ID: {contractor['id']})")
            else:
                print(f"❌ Ошибка получения списка: {response.status_code}")
        except Exception as e:
            print(f"❌ Ошибка при проверке: {e}")

if __name__ == "__main__":
    asyncio.run(add_contractors()) 
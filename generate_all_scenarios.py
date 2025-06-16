#!/usr/bin/env python3
"""
Скрипт для генерации сценариев для всех проектов без сценариев
"""

import asyncio
import httpx
import json

# Конфигурация
API_URL = "http://localhost:8000"

async def generate_scenarios_for_all_projects():
    """Генерирует сценарии для всех проектов без сценариев"""
    print("🎯 Генерация сценариев для всех проектов...")
    
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
        
        # Получаем все проекты
        try:
            response = await client.get(f"{API_URL}/projects/")
            if response.status_code == 200:
                all_projects = response.json()
                print(f"📊 Найдено проектов: {len(all_projects)}")
                
                for project in all_projects:
                    project_id = project['id']
                    project_name = project['name']
                    
                    # Проверяем, есть ли уже сценарии для этого проекта
                    scenarios_response = await client.get(f"{API_URL}/projects/{project_id}/scenarios/")
                    if scenarios_response.status_code == 200:
                        scenarios = scenarios_response.json()
                        
                        if not scenarios:
                            print(f"📝 Генерируем сценарии для проекта '{project_name}' (ID: {project_id})...")
                            
                            # Генерируем сценарии
                            generate_response = await client.post(
                                f"{API_URL}/projects/{project_id}/scenarios/generate",
                                params={"count": 3}
                            )
                            
                            if generate_response.status_code == 200:
                                generated_scenarios = generate_response.json()
                                print(f"✅ Сгенерировано {len(generated_scenarios)} сценариев для проекта '{project_name}'")
                            else:
                                print(f"❌ Ошибка генерации сценариев для проекта '{project_name}': {generate_response.status_code}")
                        else:
                            print(f"✅ Проект '{project_name}' уже имеет {len(scenarios)} сценариев")
                    else:
                        print(f"❌ Ошибка получения сценариев для проекта '{project_name}': {scenarios_response.status_code}")
                
                # Финальная проверка
                print("\n📊 Финальная проверка...")
                total_scenarios = 0
                for project in all_projects:
                    scenarios_response = await client.get(f"{API_URL}/projects/{project['id']}/scenarios/")
                    if scenarios_response.status_code == 200:
                        scenarios = scenarios_response.json()
                        total_scenarios += len(scenarios)
                        print(f"  - {project['name']}: {len(scenarios)} сценариев")
                
                print(f"\n🎉 Всего сценариев в системе: {total_scenarios}")
                
            else:
                print(f"❌ Ошибка получения проектов: {response.status_code}")
        except Exception as e:
            print(f"❌ Ошибка при обработке проектов: {e}")

if __name__ == "__main__":
    asyncio.run(generate_scenarios_for_all_projects()) 
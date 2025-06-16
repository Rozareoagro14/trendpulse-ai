#!/usr/bin/env python3
"""
Скрипт для запуска тестов TrendPulse AI
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def install_test_dependencies():
    """Устанавливает зависимости для тестов."""
    print("📦 Установка зависимостей для тестов...")
    
    test_requirements = Path("tests/requirements.txt")
    if test_requirements.exists():
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(test_requirements)], check=True)
        print("✅ Зависимости установлены")
    else:
        print("⚠️ Файл tests/requirements.txt не найден")

def run_simple_tests(api_url=None):
    """Запускает простые тесты без базы данных."""
    print("🧪 Запуск простых тестов...")
    
    if api_url:
        os.environ["API_URL"] = api_url
    
    # Запускаем только простые тесты
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_simple_project_creation.py",
        "-v",
        "--tb=short",
        "--disable-warnings"
    ]
    
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Ошибка запуска тестов: {e}")
        return False

def run_all_tests(api_url=None):
    """Запускает все тесты."""
    print("🧪 Запуск всех тестов...")
    
    if api_url:
        os.environ["API_URL"] = api_url
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--disable-warnings"
    ]
    
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Ошибка запуска тестов: {e}")
        return False

def run_tests_with_coverage(api_url=None):
    """Запускает тесты с покрытием кода."""
    print("🧪 Запуск тестов с покрытием кода...")
    
    if api_url:
        os.environ["API_URL"] = api_url
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_simple_project_creation.py",
        "-v",
        "--tb=short",
        "--disable-warnings",
        "--cov=backend",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov"
    ]
    
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Ошибка запуска тестов: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Запуск тестов TrendPulse AI")
    parser.add_argument("--api-url", default="http://localhost:8000", 
                       help="URL API для тестирования (по умолчанию: http://localhost:8000)")
    parser.add_argument("--simple", action="store_true", 
                       help="Запустить только простые тесты")
    parser.add_argument("--all", action="store_true", 
                       help="Запустить все тесты")
    parser.add_argument("--coverage", action="store_true", 
                       help="Запустить тесты с покрытием кода")
    parser.add_argument("--install-deps", action="store_true", 
                       help="Установить зависимости для тестов")
    
    args = parser.parse_args()
    
    print("🚀 TrendPulse AI - Запуск тестов")
    print(f"🔗 API URL: {args.api_url}")
    
    # Устанавливаем зависимости если нужно
    if args.install_deps:
        install_test_dependencies()
    
    success = False
    
    if args.simple:
        success = run_simple_tests(args.api_url)
    elif args.all:
        success = run_all_tests(args.api_url)
    elif args.coverage:
        success = run_tests_with_coverage(args.api_url)
    else:
        # По умолчанию запускаем простые тесты
        success = run_simple_tests(args.api_url)
    
    if success:
        print("✅ Все тесты прошли успешно!")
        return 0
    else:
        print("❌ Некоторые тесты не прошли")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
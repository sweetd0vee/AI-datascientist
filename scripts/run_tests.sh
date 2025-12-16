#!/bin/bash
# Скрипт для запуска тестов

set -e

echo "🧪 Запуск unit тестов..."

# Установка PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Запуск тестов
if [ "$1" == "--coverage" ]; then
    echo "📊 Запуск с покрытием кода..."
    pytest tests/unit/ -v --cov=src --cov-report=html --cov-report=term-missing
    echo "✅ Отчет о покрытии: htmlcov/index.html"
else
    pytest tests/unit/ -v --tb=short
fi

echo "✅ Тесты завершены!"


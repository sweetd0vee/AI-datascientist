#!/bin/bash
# Скрипт для загрузки моделей Ollama в Docker контейнер

set -e

echo "Загрузка моделей Ollama..."

# Проверка, запущен ли контейнер Ollama
if ! docker ps | grep -q ai-datascientist-ollama; then
    echo "Контейнер Ollama не запущен. Запустите сначала: docker-compose up -d"
    exit 1
fi

# Модель для анализа возможно надо взять другую модель
echo "Загрузка модели аналитика: llama2:latest"
docker exec ai-datascientist-ollama ollama pull llama2:latest || {
    echo "Не удалось загрузить модель аналитика. Проверьте название модели."
}

# Модель для генерации кода
echo "Загрузка модели кодера: qwen3-coder:latest"
docker exec ai-datascientist-ollama ollama pull qwen3-coder:latest || {
    echo "Не удалось загрузить модель кодера. Проверьте название модели."
}

echo "Модели загружены!"
echo ""
echo "Проверка загруженных моделей:"
docker exec ai-datascientist-ollama ollama list


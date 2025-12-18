.PHONY: help build up down restart logs shell-app shell-ollama setup-models clean

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Собрать образы
	docker-compose build

build-dev: ## Собрать образы для разработки
	docker-compose -f docker-compose.dev.yml build

up: ## Запустить сервисы (production)
	docker-compose up -d
	@echo "Приложение доступно на http://localhost:8501"
	@echo "Ollama доступен на http://localhost:11434"

up-dev: ## Запустить сервисы (development)
	docker-compose -f docker-compose.dev.yml up

down: ## Остановить сервисы
	docker-compose down

down-dev: ## Остановить сервисы (development)
	docker-compose -f docker-compose.dev.yml down

restart: ## Перезапустить сервисы
	docker-compose restart

logs: ## Показать логи всех сервисов
	docker-compose logs -f

logs-app: ## Показать логи приложения
	docker-compose logs -f app

logs-ollama: ## Показать логи Ollama
	docker-compose logs -f ollama

shell-app: ## Войти в контейнер приложения
	docker exec -it ai-datascientist-app bash

shell-ollama: ## Войти в контейнер Ollama
	docker exec -it ai-datascientist-ollama bash

setup-models: ## Загрузить модели Ollama
	./setup-ollama-models.sh

ps: ## Показать статус контейнеров
	docker-compose ps

clean: ## Остановить и удалить контейнеры, volumes и образы
	docker-compose down -v --rmi all
	@echo "⚠️  Все данные Ollama будут удалены!"

clean-volumes: ## Удалить только volumes (осторожно!)
	docker-compose down -v
	@echo "⚠️  Все volumes удалены, включая модели Ollama!"

rebuild: ## Пересобрать образы без кэша
	docker-compose build --no-cache

health: ## Проверить здоровье сервисов
	@echo "Проверка Ollama..."
	@curl -s http://localhost:11434/api/tags > /dev/null && echo "✅ Ollama работает" || echo "❌ Ollama не отвечает"
	@echo "Проверка приложения..."
	@curl -s http://localhost:8501/_stcore/health > /dev/null && echo "✅ Приложение работает" || echo "❌ Приложение не отвечает"


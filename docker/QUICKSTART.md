# Быстрый старт с Docker

## Минимальные требования

- Docker 20.10+
- Docker Compose 2.0+
- Минимум 8GB RAM (для моделей Ollama)
- 20GB свободного места на диске (для моделей)

## Быстрый запуск

### 1. Клонирование и переход в директорию
```bash
cd /path/to/AI-datascientist
cd docker
```

### 2. Запуск сервисов
```bash
# Production режим
make up
# или
docker-compose up -d

# Development режим (с hot-reload)
make up-dev
# или
docker-compose -f docker-compose.dev.yml up
```

### 3. Загрузка моделей Ollama
После запуска контейнеров загрузите модели:

```bash
make setup-models
# или
./setup-ollama-models.sh
```

### 4. Открыть приложение
Откройте в браузере: http://localhost:8501

## Основные команды

```bash
# Показать все доступные команды
make help

# Просмотр логов
make logs

# Остановка
make down

# Перезапуск
make restart

# Проверка здоровья
make health
```

## Структура сервисов

- **app** (порт 8501) - Streamlit приложение
- **ollama** (порт 11434) - Ollama сервер с моделями

## Troubleshooting

### Порт занят
```bash
# Проверить, что использует порт
lsof -i :8501
lsof -i :11434

# Остановить процесс или изменить порты в docker-compose.yml
```

### Модели не загружаются
```bash
# Проверить статус Ollama
docker exec ai-datascientist-ollama ollama list

# Загрузить модели вручную
docker exec ai-datascientist-ollama ollama pull t-pro-it-1.0-q8_0.gguf:latest
docker exec ai-datascientist-ollama ollama pull qwen3-coder:latest
```

### Приложение не подключается к Ollama
Проверьте переменные окружения в `docker-compose.yml`:
- `OLLAMA_BASE_URL=http://ollama:11434` (важно: имя сервиса, не localhost!)

## Остановка и очистка

```bash
# Остановить сервисы
make down

# Остановить и удалить volumes (удалит модели!)
make clean-volumes

# Полная очистка (удалит всё)
make clean
```

## Production deployment

Для production рекомендуется:

1. Использовать `.env` файл для конфигурации
2. Настроить reverse proxy (nginx/traefik)
3. Использовать Docker secrets
4. Настроить мониторинг
5. Регулярно обновлять образы

Подробнее см. `README.md` в этой директории.

